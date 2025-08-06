"""
from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify
from models.bug_detection import detect_bug
from models.bug_error_class import classify_error_type
from models.bug_fixing import suggest_fixes  

detect_bp = Blueprint("detect", __name__)

@detect_bp.route("/", methods=["GET", "POST"])
def index():
    
    if request.method == "POST":
        data = request.get_json()

        if not data or "code" not in data:
            return jsonify({"error": "No code provided!"}), 400

        code_snippet = data["code"].strip()

        if not code_snippet:
            return jsonify({"error": "Please enter valid code!"}), 400

        try:
            result = detect_bug(code_snippet)
            error_type = classify_error_type(code_snippet)
            fix_suggestions = suggest_fixes(code_snippet)

            # Store in session
            session["code_snippet"] = code_snippet
            session["error_type"] = error_type
            session["fix_suggestions"] = fix_suggestions  

            return jsonify({"redirect": url_for("detect.result_page")})

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "API unavailable after multiple retries. Please try again later."}), 500

    return render_template("index.html")


@detect_bp.route("/result")
def result_page():
    
    if "error_type" not in session or "code_snippet" not in session:
        return redirect(url_for("detect.index"))

    return render_template("results.html",
                           code=session["code_snippet"],
                           error_type=session["error_type"],
                           fix_suggestions=session.get("fix_suggestions", [])
    )

"""
"""

from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify
from models.bug_detection import detect_bug
from models.bug_error_class import classify_error_type
from models.bug_fixing import suggest_fixes  

detect_bp = Blueprint("detect", __name__)

@detect_bp.route("/", methods=["GET", "POST"])
def index():
    
    if request.method == "POST":
        data = request.get_json()

        if not data or "code" not in data:
            return jsonify({"error": "No code provided!"}), 400

        code_snippet = data["code"].strip()

        if not code_snippet:
            return jsonify({"error": "Please enter valid code!"}), 400

        try:
            bug_result = detect_bug(code_snippet)

            # ✅ Always return all three results
            bug_detected = "Bug Detected" in bug_result  # True if a bug is found
            error_type = classify_error_type(code_snippet) if bug_detected else "No Error"
            fix_suggestions = suggest_fixes(code_snippet) if bug_detected else ["No fixes needed. Code is bug-free."]

            # Store results in session
            session["code_snippet"] = code_snippet
            session["bug_detected"] = "Yes" if bug_detected else "No"
            session["error_type"] = error_type
            session["fix_suggestions"] = fix_suggestions  

            return jsonify({"redirect": url_for("detect.result_page")})

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "API unavailable after multiple retries. Please try again later."}), 500

    return render_template("index.html")


@detect_bp.route("/result")
def result_page():
    if "error_type" not in session or "code_snippet" not in session:
        return redirect(url_for("detect.index"))

    return render_template("results.html",
                           code=session["code_snippet"],
                           bug_detected=session["bug_detected"],
                           error_type=session["error_type"],
                           fix_suggestions=session.get("fix_suggestions", [])
    )
"""








from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify
import logging
from models.bug_detection import detect_bug
from models.bug_fixing import suggest_fixes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

detect_bp = Blueprint("detect", __name__)

@detect_bp.route("/", methods=["GET", "POST"])
def index():
    """Home page with code input."""
    if request.method == "POST":
        # Validate request data
        if not request.is_json:
            return jsonify({"error": "Invalid content type, expected JSON"}), 400
            
        data = request.get_json()
        if not data or "code" not in data:
            return jsonify({"error": "No code provided"}), 400

        code_snippet = data["code"].strip()
        if not code_snippet:
            return jsonify({"error": "Empty code snippet provided"}), 400

        try:
            # Perform bug detection
            detection_result = detect_bug(code_snippet)
            
            # Initialize session data
            session.clear()
            session["code_snippet"] = code_snippet
            session["detection_result"] = detection_result
            session["fix_result"] = None
            
            # Only generate fixes if bugs were detected
            if detection_result['status'] == 'Bug Detected':
                try:
                    fix_result = suggest_fixes(code_snippet)
                    session["fix_result"] = fix_result
                except Exception as fix_error:
                    logger.error(f"Fix suggestion failed: {fix_error}")
                    session["fix_result"] = {
                        'status': 'error',
                        'message': 'Could not generate fixes'
                    }

            return jsonify({
                "redirect": url_for("detect.result_page"),
                "detection_result": detection_result,
                "has_fixes": session["fix_result"] is not None
            })

        except Exception as e:
            logger.error(f"Bug detection error: {str(e)}", exc_info=True)
            return jsonify({
                "error": "An error occurred during analysis",
                "details": str(e)
            }), 500

    return render_template("index1.html")

@detect_bp.route("/result")
def result_page():
    """Displays bug detection results."""
    try:
        # Safely get session data with defaults
        context = {
            "code": session.get("code_snippet", ""),
            "detection_result": session.get("detection_result", {
                'status': 'Error',
                'message': 'No analysis results found'
            }),
            "fix_result": session.get("fix_result", None),
            "has_bug": session.get("detection_result", {}).get('status') == 'Bug Detected',
            "has_fixes": session.get("fix_result") is not None
        }
        
        if not context["code"]:
            return redirect(url_for("detect.index"))

        return render_template("results.html", **context)

    except Exception as e:
        logger.error(f"Result page error: {str(e)}", exc_info=True)
        return render_template("error.html", 
                           message="An error occurred while loading results",
                           error_details=str(e)), 500

@detect_bp.route("/about")
def about():
    """About Us Page"""
    return render_template("about.html")

@detect_bp.route("/services")
def services():
    """Services Page"""
    return render_template("services.html")

@detect_bp.route("/index")
def home_page():
    """Index Page"""
    return render_template("index.html")