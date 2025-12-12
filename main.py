"""
Standalone DMCompVerify API
Simple API to process DMCompVerify challenges on a separate VPS
"""
import os
import argparse
import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from ctypes import CDLL, c_longlong, POINTER, c_void_p, c_char_p

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="DMCompVerify API",
    description="Standalone API for processing DMCompVerify challenges",
    version="1.0.0"
)


class DMCompVerifyWrapper:
    """Wrapper for libdmcompverify.so"""
    
    def __init__(self, lib_path: str = "/usr/lib/libdmcompverify.so"):
        """
        Initialize the DMCompVerify wrapper.
        
        Args:
            lib_path: Path to libdmcompverify.so library
        """
        if not os.path.exists(lib_path):
            raise FileNotFoundError(f"Library not found: {lib_path}")
        
        self._lib = CDLL(lib_path)
        self._setup_lib_functions()
    
    def _setup_lib_functions(self):
        """Set up function signatures for the library"""
        self._lib.DMCompVerify_new.argtypes = [c_longlong, c_longlong]
        self._lib.DMCompVerify_new.restype = POINTER(c_void_p)
        
        self._lib.processChallengeResult.argtypes = [POINTER(c_void_p), c_longlong, c_char_p]
        self._lib.processChallengeResult.restype = c_char_p
        
        self._lib.getUUID.argtypes = [c_void_p]
        self._lib.getUUID.restype = c_char_p
        
        self._lib.free.argtypes = [c_void_p]
        self._lib.free.restype = None
    
    def process_challenge(self, dim_n: int, dim_k: int, seed: int, cipher_text: str) -> str:
        """
        Process a DMCompVerify challenge.
        
        Args:
            dim_n: Matrix dimension n
            dim_k: Matrix dimension k
            seed: Random seed
            cipher_text: Encrypted challenge text
        
        Returns:
            str: UUID extracted from the challenge
        """
        # Create a new DMCompVerify object
        verifier_ptr = self._lib.DMCompVerify_new(dim_n, dim_k)
        
        try:
            # Process the challenge
            self._lib.processChallengeResult(verifier_ptr, seed, cipher_text.encode('utf-8'))
            
            # Get the UUID
            uuid_ptr = self._lib.getUUID(verifier_ptr)
            if uuid_ptr:
                uuid = c_char_p(uuid_ptr).value
                return uuid.decode('utf-8') if uuid else ""
            return ""
        finally:
            # Free resources
            self._lib.free(verifier_ptr)


# Initialize wrapper (lazy loading)
_wrapper: DMCompVerifyWrapper | None = None


def get_wrapper() -> DMCompVerifyWrapper:
    """Get or create the DMCompVerify wrapper"""
    global _wrapper
    if _wrapper is None:
        lib_path = os.getenv("LIBDMCOMPVERIFY_PATH", "/usr/lib/libdmcompverify.so")
        _wrapper = DMCompVerifyWrapper(lib_path)
    return _wrapper


# Request/Response Models
class ChallengeRequest(BaseModel):
    """Request model for challenge processing"""
    dim_n: int
    dim_k: int
    seed: int
    cipher_text: str


class ChallengeResponse(BaseModel):
    """Response model for challenge processing"""
    uuid: str
    success: bool
    message: str | None = None


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "DMCompVerify API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    try:
        wrapper = get_wrapper()
        return {
            "status": "healthy",
            "library_loaded": True
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "library_loaded": False,
            "error": str(e)
        }


@app.post("/process", response_model=ChallengeResponse)
async def process_challenge(request: ChallengeRequest):
    """
    Process a DMCompVerify challenge.
    
    Args:
        request: Challenge request with dim_n, dim_k, seed, and cipher_text
    
    Returns:
        ChallengeResponse: UUID extracted from the challenge
    """
    try:
        wrapper = get_wrapper()
        
        logger.info(f"Processing challenge: dim_n={request.dim_n}, dim_k={request.dim_k}, seed={request.seed}")
        
        uuid = wrapper.process_challenge(
            dim_n=request.dim_n,
            dim_k=request.dim_k,
            seed=request.seed,
            cipher_text=request.cipher_text
        )
        
        if uuid:
            logger.info(f"Challenge processed successfully, UUID: {uuid}")
            return ChallengeResponse(
                uuid=uuid,
                success=True,
                message="Challenge processed successfully"
            )
        else:
            logger.warning("Challenge processed but no UUID returned")
            return ChallengeResponse(
                uuid="",
                success=False,
                message="No UUID returned from challenge"
            )
    
    except FileNotFoundError as e:
        logger.error(f"Library not found: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Library not found: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Error processing challenge: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process challenge: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    parser = argparse.ArgumentParser(description="DMCompVerify API Server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--lib-path", type=str, default="/usr/lib/libdmcompverify.so", help="Path to libdmcompverify.so")
    
    args = parser.parse_args()
    
    # Set library path as environment variable
    os.environ["LIBDMCOMPVERIFY_PATH"] = args.lib_path
    
    logger.info(f"Starting DMCompVerify API on {args.host}:{args.port}")
    logger.info(f"Library path: {args.lib_path}")
    
    uvicorn.run(app, host=args.host, port=args.port)

