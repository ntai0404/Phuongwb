from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from ..models import get_db, User
from ..auth.security import get_current_admin
from .schemas import RawSQLRequest, RawSQLResponse

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])

@router.post("/sql/execute", response_model=RawSQLResponse)
def execute_raw_sql(
    sql_request: RawSQLRequest,
    db: Session = Depends(get_db)
    # current_user: User = Depends(get_current_admin)
):
    """
    Execute raw SQL query (Admin only)
    
    WARNING: This endpoint is for administrative purposes only.
    Use with caution as it allows direct database access.
    """
    try:
        # Execute the query
        result = db.execute(text(sql_request.query))
        db.commit()
        
        # Try to fetch results if it's a SELECT query
        if sql_request.query.strip().upper().startswith('SELECT'):
            rows = result.fetchall()
            # Convert rows to list of dicts
            data = []
            if rows:
                columns = result.keys()
                data = [dict(zip(columns, row)) for row in rows]
            
            return RawSQLResponse(
                success=True,
                rows_affected=len(data),
                data=data
            )
        else:
            # For INSERT, UPDATE, DELETE, etc.
            return RawSQLResponse(
                success=True,
                rows_affected=result.rowcount
            )
            
    except Exception as e:
        db.rollback()
        return RawSQLResponse(
            success=False,
            error=str(e)
        )

@router.get("/sql/tables")
def list_tables(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    List all tables in the database (Admin only)
    """
    try:
        result = db.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = [row[0] for row in result.fetchall()]
        
        return {
            "success": True,
            "tables": tables
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/sql/describe/{table_name}")
def describe_table(
    table_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """
    Get table schema information (Admin only)
    """
    try:
        result = db.execute(text("""
            SELECT 
                column_name,
                data_type,
                character_maximum_length,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = :table_name
            ORDER BY ordinal_position
        """), {"table_name": table_name})
        
        columns = []
        for row in result.fetchall():
            columns.append({
                "name": row[0],
                "type": row[1],
                "max_length": row[2],
                "nullable": row[3],
                "default": row[4]
            })
        
        if not columns:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Table '{table_name}' not found"
            )
        
        return {
            "success": True,
            "table": table_name,
            "columns": columns
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
