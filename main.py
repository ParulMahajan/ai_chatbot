import os
import sys
import uvicorn
from pypandoc import download_pandoc
from util_ai.logger import logger
from dotenv import load_dotenv


def main():
    try:
        load_dotenv()
        download_pandoc()
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
        logger.info("Starting Chatbot Application")
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=8080,
            reload=True,
            log_level="info"
        )

    except KeyboardInterrupt:
        logger.info("Application stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Application failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure working directory is project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)

    main()