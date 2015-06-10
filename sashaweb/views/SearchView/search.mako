<%inherit file="sashaweb:templates/base__search.mako"/>

<%!
    from sasha import sasha_configuration, Event, Instrument
    from sashaweb.helpers import EventHelper, FingeringHelper, InstrumentHelper
    from sashaweb.helpers import ChordNotationHelper, ChromaNotationHelper, MP3AudioHelper
    from sashaweb.helpers import FingeringNotationHelper, PartialTrackingPlotHelper
%>

<%block name="page_title">
<div id="page_title" class="grid_12">Searching Recordings</div>
</%block>

<div id="search" class="clearfix">

<%block name="searchbar">
    <form id="searchbar" class="grid_2" action="${search_action}" method="get">
        <div class="grid_2 alpha">
            <button type="submit">SEARCH</button>
        </div>
        <div class="grid_2 category alpha">
            <div class="label">WITH PITCHES:</div>
            <div id="with_pitches" class="items">
                <input type="text" name="with_pitches" placeholder="i.e. eqs4 ef6 gs5" value="${with_pitches}"/>
            </div>
        </div>
        <div class="grid_2 category alpha">
            <div class="label">W/O PITCHES:</div>
            <div id="without_pitches" class="items">
                <input type="text" name="without_pitches" placeholder="i.e. c4 ef6 gs5" value="${without_pitches}"/>
            </div>
        </div>
        <div class="grid_2 category alpha">
            <div class="label">WITH PITCH CLASSES:</div>
            <div id="with_pitch_classes" class="items">
                <input type="text" name="with_pitch_classes" placeholder="i.e. cs e gqf" value="${with_pitch_classes}"/>
            </div>
        </div>
        <div class="grid_2 category alpha">
            <div class="label">W/O PITCH CLASSES:</div>
            <div id="without_pitch_classes" class="items">
                <input type="text" name="without_pitch_classes" placeholder="i.e. dqf f bf" value="${without_pitch_classes}"/>
            </div>
        </div>
    </form>
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

<%block name="other">
</%block>
