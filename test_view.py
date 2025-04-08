# Save this as test_view.py in your project root

from django.http import HttpResponse

def test_view(request):
    """
    A simple view to test that the web server is responding to requests.
    Access at /test/
    """
    return HttpResponse(
        """
        <html>
            <head><title>Django Server Test</title></head>
            <body>
                <h1>Your Django server is running!</h1>
                <p>If you can see this page, the basic web server functionality is working.</p>
                <p>Now we need to troubleshoot why the login page isn't loading.</p>
            </body>
        </html>
        """
    )