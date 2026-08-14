from bs4 import BeautifulSoup
import logging
import os

# import ML vision components
try:
    from ML_vision.predict import suggest_alt_text_for_img_tag

    ML_VISION_AVAILABLE = True
except ImportError:
    ML_VISION_AVAILABLE = False
    logging.warning(
        "ML_vision modules not found. AI-powered alt text suggestions will be disabled."
    )


def analyze_image_tag(tag):
    issues = []

    # Extract image source for ML prediction if needed
    img_src = tag.get("src", "")

    # Check if alt attribute is missing
    def is_alt_missing(tag):
        return not tag.has_attr("alt")

    # Check if alt text is vague
    def is_alt_vague(tag):
        vague_terms = ["image", "photo", "picture", "graphic", "logo", "icon"]
        alt_text = tag.get("alt", "").strip().lower()
        return (
            alt_text in vague_terms
            or len(alt_text) < 3
            or alt_text.endswith((".jpg", ".png", ".jpeg", ".gif"))
        )

    # Apply checks
    if is_alt_missing(tag):
        issue = {
            "module": "imagealt",
            "element": str(tag),
            "issue": "Missing alt attribute on image",
            "help": "Add a meaningful alt attribute to describe the image for screen readers.",
        }

        # Add AI suggestion if available
        if ML_VISION_AVAILABLE and img_src:
            try:
                suggestion = suggest_alt_text_for_img_tag(img_src)
                if suggestion.get("success") and suggestion.get("suggested_alt"):
                    issue["suggestion"] = (
                        f"AI Suggested Alt Text: '{suggestion['suggested_alt']}'"
                    )
            except Exception as e:
                logging.error(f"Error generating AI suggestion: {e}")

        issues.append(issue)

    elif is_alt_vague(tag):
        issue = {
            "module": "imagealt",
            "element": str(tag),
            "issue": "alt text is not Descriptive",
            "help": "Avoid vague alt text like 'image' or 'photo'; describe the image content clearly.",
        }

        # Add AI suggestion if available
        if ML_VISION_AVAILABLE and img_src:
            try:
                suggestion = suggest_alt_text_for_img_tag(img_src)
                if suggestion.get("success") and suggestion.get("suggested_alt"):
                    issue["suggestion"] = (
                        f"AI Suggested Alt Text: '{suggestion['suggested_alt']}'"
                    )
            except Exception as e:
                logging.error(f"Error generating AI suggestion: {e}")

        issues.append(issue)

    return issues
