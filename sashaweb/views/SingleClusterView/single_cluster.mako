<%inherit file="sashaweb:templates/base__search.mako"/>

<%!
    from pyramid.url import route_url, current_route_url
    from sasha import SASHA, Event, Instrument
    from sashaweb.helpers import EventHelper, FingeringHelper, InstrumentHelper
    from sashaweb.helpers import ChordNotationHelper, MP3AudioHelper, ClusterHelper
    from sashaweb.helpers import FingeringNotationHelper
%>

<%block name="page_title">
    <div id="page_title" class="grid_12">
        ${ClusterHelper(cluster, request).feature} Cluster No.${cluster.cluster_id}
% if instrument is None:
        (All Instruments)
% else:
        (Filtered by ${InstrumentHelper(instrument, request).link})
% endif
    </div>
</%block>

<div id="search" class="clearfix">

<%block name="searchbar">
    <div class="grid_2">

        <div class="grid_2 alpha bottom divider">
            <div class="bottom divider">INSTRUMENTS</div>
            <a href="${current_route_url(request)}" class="button">All Instruments</a>
            <a href="${current_route_url(request, _query={'instrument': 'alto_saxophone'})}" class="button">Alto Saxophone</a>
            <a href="${current_route_url(request, _query={'instrument': 'soprano_saxophone'})}" class="button lastbutton">Soprano Saxophone</a>
        </div>

        <div class="grid_2 alpha clusters bottom divider">
            <div class="bottom divider">CHROMA</div>
            <ul>
% for cluster in clusters['chroma']:
                <li>${ClusterHelper(cluster, request).link}</li>
% endfor
            </ul>       
        </div>

        <div class="grid_2 alpha clusters bottom">
            <ul>
            <div class="bottom divider">CONSTANT-Q</div>
% for cluster in clusters['constant_q']:
                <li>${ClusterHelper(cluster, request).link}</li>
% endfor
            </ul>       
        </div>

        <div class="grid_2 alpha clusters bottom">
            <ul>
            <div class="bottom divider">MFCC</div>
% for cluster in clusters['mfcc']:
                <li>${ClusterHelper(cluster, request).link}</li>
% endfor
            </ul>       
        </div>

    </div>
</%block>

% if len(paginator):

<div id="results" class="grid_10">

    <nav class="pagination">
        ${paginator.pager('$link_first $link_previous ~3~ $link_next $link_last', show_if_single_page=True)}
        <span class="pager_summary">${paginator.pager('($first_item through $last_item of $item_count)', show_if_single_page=True)}</span>
    </nav>

    <div id="events" class="clearfix">
%for i, event in enumerate(paginator):
    % if i % 5 == 0 and 0 < i:
        <div class="clearfix grid_10 divider alpha omega"></div>
    % endif
    % if i % 5 == 0:
        <div id="${event.canonical_name}" class="event grid_2 alpha">
    % elif i % 5 == 4:
        <div id="${event.canonical_name}" class="event grid_2 omega">
    % else:
        <div id="${event.canonical_name}" class="event grid_2">
    % endif
            <div class="annotation id">${EventHelper(event, request).numbered_link}</div>
            <div class="annotation instrument">${InstrumentHelper(event, request).link}</div>
            <div class="annotation audio">${MP3AudioHelper(event, request).audio}</div>
            <div class="annotation notations">
                ${FingeringNotationHelper(event, request).image_link}
                ${ChordNotationHelper(event, request).image_link}
            </div>
        </div>
%endfor
    </div>

    <nav class="pagination">
        ${paginator.pager('$link_first $link_previous ~3~ $link_next $link_last', show_if_single_page=True)}
        <span class="pager_summary">${paginator.pager('($first_item through $last_item of $item_count)', show_if_single_page=True)}</span>
    </nav>
</div>

% else:

    <div class="results grid_10">
        <h1>Nothing found.</h1>
        <h2>Insert coin to try again.</h2>
    </div>

% endif

    <div class="grid_12 divider"></div>

</div>

