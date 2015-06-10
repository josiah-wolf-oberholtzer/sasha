<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr" lang="en-US">

<head profile="http://gmpg.org/xfn/11">
    <title>${page_title}</title>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
    <link rel="icon" type="image/png" href="${request.static_url('sashaweb:static/img/favicon.ico')}"/>
    <link rel="stylesheet" href="${request.static_url('sashaweb:static/css/normalize.css')}"/>
    <link rel="stylesheet" href="${request.static_url('sashaweb:static/css/960_12_col.css')}"/>
    <link rel="stylesheet" href="${request.static_url('sashaweb:static/css/sasha.css')}"/>
    <script type="text/javascript" src="${request.static_url('sashaweb:static/js/jquery-1.7.1.min.js')}"></script>
    <script type="text/javascript" src="${request.static_url('sashaweb:static/js/audio-player.js')}"></script>  
    <script type="text/javascript">  
        AudioPlayer.setup("${request.static_url('sashaweb:static/swf/player.swf')}", {
            animation: "no",
            noinfo: "yes",
            transparentpagebg: "yes",
            width: 130,
        });
  </script>
</head>

<body class="${body_class}">
<div id="wrap" class="container_12">

<header id="header" class="clearfix">
    <hgroup id="masthead" class="grid_12">
        <h1 id="site_title">
            <a href="/">
                S<span class="grey">.</span>A<span class="grey">.</span>S<span class="grey">.</span>H<span class="grey">.</span>A<span class="grey">.</span>
            </a>
        </h1>
        <h2 id="site_subtitle">Saxophone Acoustic Search and Heuristic Analysis</h2>
    </hgroup>
    <nav id="mainmenu" class="grid_12">
        <ul>
            <li><a href="/">MAIN</a></li>
            <li class="search"><a href="/search/">SEARCH</a></li>
            <li class="clusters"><a href="/clusters/">CLUSTERS</a></li>
            <li><a href="/random/">RANDOM</a></li>
            <li><a href="/docs/">DOCS</a></li>
            <li><a href="/about/">ABOUT</a></li>
        </ul>
    </nav>
% if request.session.peek_flash():
    <aside id="flash" class="grid_12">
        <ul>
        <% flash = request.session.pop_flash() %>
        % for message in flash:
            <li>${message}</li>
        % endfor
        </ul>
    </aside>
% endif
</header>

<div id="main" class="clearfix">
    ${next.body( )}
</div>

<%!
    import datetime
%>

<footer id="footer" class="clearfix">
    <div id="copyright" class="grid_12">
        All content copyright 2010-${datetime.datetime.today().year}
        <a href="http://eliotgattegno.com">Eliot Gattegno</a>
        and
        <a href="http://josiahwolfoberholtzer.com">Josiah Oberholtzer</a>.
    </div>
<footer>

</div>
</body>
</html>
