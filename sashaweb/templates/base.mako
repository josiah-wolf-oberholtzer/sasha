<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr" lang="en-US">
<%!
    from sasha.tools import domaintools
    from sashaweb import helpers
    import datetime
%>
<head profile="http://gmpg.org/xfn/11">
    <title>${title}</title>
    <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"/>
    <meta property="og:description" content="Saxophone Acoustic Search and Heuristic Analysis" />
    <meta property="og:image" content="http://sasha.mbrsi.org/assets/plots/event__9ff9e473eb974e9576739647ac0b72ae__partials.png" />
    <meta property="og:site_name" content="S.A.S.H.A." />
    <meta property="og:title" content="${title}" />
    <meta property="og:url" content="http://sasha.mbrsi.org/search/" />
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
    <!--<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">-->
    <link rel="icon" type="image/png" href="${request.static_url('sashaweb:static/img/favicon.ico')}"/>
    <link rel="stylesheet" href="${request.static_url('sashaweb:static/css/sasha.v2.css')}"/>
</head>

<body class="${body_class}">

<nav class="navbar navbar-default navbar-fixed-top navbar-inverse">
    <div class="container">
        <div class="navbar-header">
            <button type="button" class="navbar-toggle collapsed" 
                data-toggle="collapse" data-target="#navbar" 
                aria-expanded="false" aria-controls="navbar">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
            </button>
            <a class="navbar-brand" href="/">S.A.S.H.A.</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
            <ul class="nav navbar-nav">
                <li><a href="/search/">Search</a></li>
                <li class="dropdown">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown" 
                        role="button" aria-haspopup="true" 
                        aria-expanded="false">Instruments<span class="caret"></span></a>
                    <ul class="dropdown-menu">
                    % for instrument in domaintools.Instrument.with_events():
                        <% helper = helpers.InstrumentHelper(instrument, request) %>
                        <li><a href="${helper.url}">${helper.name}</a></li>
                    % endfor
                    </ul>
                </li>
                <li class="dropdown">
                    <a href="#" class="dropdown-toggle" data-toggle="dropdown" 
                        role="button" aria-haspopup="true" 
                        aria-expanded="false">Clusters<span class="caret"></span></a>
                    <ul class="dropdown-menu">
                    % for cluster in domaintools.Cluster.get():
                        <% helper = helpers.ClusterHelper(cluster, request) %>
                        <li><a href="${helper.url}">${helper.name.decode('utf-8')}</a></li>
                    % endfor
                    </ul>
                </li>
                <li><a href="/random/">Random</a></li>
            </ul>
            <ul class="nav navbar-nav navbar-right">
                <li><a href="/docs/">Docs</a></li>
                <li><a href="/about/">About</a></li>
            </ul>
        </div>
    </div>
</nav>

<div class="container">

% if request.session.peek_flash():
<% flash = request.session.pop_flash() %>
% for message in flash:
    <div class="alert alert-danger alert-dismissible" role="alert">
        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
            <span aria-hidden="true">&times;</span>
        </button>
        ${message}
    </div>
% endfor
% endif

${next.body()}

</div>

<footer class="sasha-footer" role="contentinfo">
    <div class="container">
    <p>
        Performed by 
        <a href="http://eliotgattegno.com">Eliot Gattegno</a>
        and engineered by
        <a href="http://josiahwolfoberholtzer.com">Josiah Oberholtzer</a>.
    </p>
    <p>All content copyright 2010-${datetime.datetime.today().year}.</p>
    </div>
</footer>

<script>
    (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
    })(window,document,'script','//www.google-analytics.com/analytics.js','ga');
    ga('create', 'UA-4612344-3', 'auto');
    ga('send', 'pageview');
</script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>

</body>
</html>