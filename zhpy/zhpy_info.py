"""
zhpy Complete Version Information

This is the MIT license:
http://www.opensource.org/licenses/mit-license.php

Copyright (c) 2007 Fred Lin and contributors. zhpy is a trademark of Fred Lin.

Permission is hereby granted, free of charge, to any person obtaining a copy 
of this software and associated documentation files (the "Software"), to 
deal in the Software without restriction, including without limitation the 
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
sell copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in 
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
THE SOFTWARE.
"""

import pkg_resources

entrypoints = {"TW Keyword Dictionaries":"zhpy.twdict",
                "CN Keyword Dictionaries":"zhpy.cndict"}
    
def retrieve_info():
    """
    retrieve package and plugins info
    """
    packages=['%s' % i for i in pkg_resources.require("zhpy")]
    plugins = {}
    for name, pointname in entrypoints.items():
        plugins[name] = ["%s (%s)" % (entrypoint.name, str(entrypoint.dist))
            for entrypoint in pkg_resources.iter_entry_points(pointname)
        ]
    return packages, plugins

def info():
    """
    from TurboGears2 tginfo command
    """
    print """zhpy Complete Version Information
    
zhpy requires:
    """
    
    packages, plugins = retrieve_info()
    for p in packages:
        print '*', p
    
    print "\nzhpy extends:"
    for name, pluginlist in plugins.items():
        print "\n", name, "\n"
        for plugin in pluginlist:
            print '*', plugin