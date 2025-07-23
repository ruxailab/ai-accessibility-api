def AriaAligner():
    """
    Provides semantic information for custom or 
    non-standard UI components to assistive technologies.
    
    Html tags that Consists of Aria labels:
    
    1> button without text 
    <button aria-label="Close menu">
        <svg>...</svg>
    </button>
    
    2> 
    Inputs without <label> tag
                <input type="text" aria-label="Search website">

    3>
    <a href="/download" aria-label="Download PDF">
        <i class="fa fa-download"></i>
    </a>

    4>
    <nav aria-label="Main navigation">
            ...
    </nav>
    5>
        <a href="/about" aria-label="Learn more about us">About</a>

    
    """
    print("Aria Aligner")