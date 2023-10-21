from fastapi import HTTPException, status


def http_exception_403(detail: str):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


def http_exception_404(detail: str):
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


def http_exception_401(detail: str):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
    )


def socket_exception_connection_refused(detail: str):
    raise ConnectionRefusedError(detail)
