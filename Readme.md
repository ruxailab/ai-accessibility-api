AI-Powered Web Accessibility Tool
This repository contains the core modules for an AI-powered tool designed to enhance web accessibility testing by automating the detection and suggestion of fixes for common accessibility issues. By leveraging advanced AI models like Gemini, this tool aims to provide more intelligent and context-aware insights than traditional rule-based checkers.

Core Modules
1. Image Alt Text
Purpose: Ensures images are understandable to users relying on screen readers.

AI Integration: Uses ML model for (Image-to-text) conversion then Utilizes Gemini to  generate highly descriptive and contextually appropriate alt text suggestions.

2. Color Contrast
Purpose: Verifies that text and essential graphical elements have sufficient contrast for readability, adhering to WCAG guidelines.

Methodology: Calculates contrast ratios based on foreground and background color luminance. Future enhancements may include AI for complex background detection.

3. ARIA Labels and Roles
Purpose: Provides semantic information for custom or non-standard UI components to assistive technologies.

AI Integration: Gemini analyzes HTML snippets to infer the intended purpose of elements and suggests the most accurate ARIA labels and roles. This also covers Input Field Labels.

4. Link Text Readability and Context
Purpose: Ensures links are descriptive and make sense out of context for all users, particularly those navigating with screen readers.

AI Integration: AI (Gemini) evaluates link text in relation to its surrounding content and target page, identifying vague phrases and suggesting clearer alternatives.

5. Heading Structure and Semantics
Purpose: Validates the logical hierarchy and correct semantic markup of headings (H1-H6) for improved content navigation.

Methodology: Analyzes the Document Object Model (DOM) structure and text content to detect skipped levels or visually styled headings without proper tags. AI could further refine content-based suggestions.