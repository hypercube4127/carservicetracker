import os
import sys
import logging
from app import app, db
from flask_migrate import upgrade

logger = logging.getLogger()
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)

DEBUG_MODE = os.getenv("DEBUG_MODE", 'False').lower() == "true"
AUTO_RELOAD = os.getenv("AUTO_RELOAD", 'False').lower() == "true"

def main():
  port = int(os.getenv('FLASK_PORT', 5000))

  with app.app_context():
    upgrade()

  if DEBUG_MODE and os.getenv('WERKZEUG_RUN_MAIN') is None:
    import debugpy
    logger.info("Start Debugger")
    debugpy.configure(subProcess=True)
    debugpy.listen(("0.0.0.0", 5678))
    logger.info("Debugger listen on 5678")
    debug_wait_for_client = os.getenv('DEBUG_WAIT_FOR_CLIENT', 'False').lower() == 'true'
    if debug_wait_for_client:
      logger.warning("Debugger started. Waiting for the client to start the application...")
      debugpy.wait_for_client()
  
  app.run(debug=False, port=port, host='0.0.0.0', use_reloader=True)
