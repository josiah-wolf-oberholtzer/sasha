<%inherit file="sashaweb:templates/base.mako"/>
<%!
    from sasha import sasha_configuration
    from sasha.tools.domaintools import Event
    from sasha.tools.domaintools import Instrument
    from sashaweb.helpers.EventHelper import EventHelper
    from sashaweb.helpers.FingeringHelper import FingeringHelper
    from sashaweb.helpers.InstrumentHelper import InstrumentHelper
    from sashaweb.helpers.ChordNotationHelper import ChordNotationHelper
    from sashaweb.helpers.ChromaNotationHelper import ChromaNotationHelper
    from sashaweb.helpers.MP3AudioHelper import MP3AudioHelper
    from sashaweb.helpers.FingeringNotationHelper import FingeringNotationHelper
    from sashaweb.helpers.PartialTrackingPlotHelper import PartialTrackingPlotHelper
%>

<%block name="searchbar">
<form action="${search_action}" method="get" class="form-horizontal">
    <div class="form-group">
        <div class="col-sm-offset-3 col-sm-9">
            <button type="submit" class="btn btn-default">Search</button>
        </div>
    </div>
    <div class="form-group">
        <label class="control-label col-sm-3">Include pitches:</label>
        <div class="col-sm-9">
            <input type="text" class="form-control" name="with_pitches" placeholder="i.e. eqs4 ef6 gs5" value="${with_pitches}"/>
        </div>
    </div>
    <div class="form-group">
        <label class="control-label col-sm-3">Exclude pitches:</label>
        <div class="col-sm-9">
            <input type="text" class="form-control" name="without_pitches" placeholder="i.e. c4 ef6 gs5" value="${without_pitches}"/>
        </div>
    </div>
    <div class="form-group">
        <label class="control-label col-sm-3">Include pitch-classes:</label>
        <div class="col-sm-9">
            <input type="text" class="form-control" name="with_pitch_classes" placeholder="i.e. cs e gqf" value="${with_pitch_classes}"/>
        </div>
    </div>
    <div class="form-group">
        <label class="control-label col-sm-3">Exclude pitch-classes:</label>
        <div class="col-sm-9">
            <input type="text" class="form-control" name="without_pitch_classes" placeholder="i.e. dqf f bf" value="${without_pitch_classes}"/>
        </div>
    </div>
</form>
</%block>

% if len(paginator):
<nav class="row">
    <div class="col-lg-12 text-center">
        <ul class="pagination">
            ${paginator.pager(
                '$link_first $link_previous ~3~ $link_next $link_last', 
                show_if_single_page=True,
                )}
        </ul>
    </nav>
</nav>

<div class="row">
% for i, event in enumerate(paginator):
    % if 0 < i and i % 4 == 0:
    </div>
    <div class="row">
    % endif
    <div id="${event.canonical_name}" class="col-sm-3 col-xs-6">
        ${EventHelper(event, request).numbered_link}
        ${InstrumentHelper(event, request).link}
        <div>${MP3AudioHelper(event, request).audio}</div>
        <div class="text-center">
            ${FingeringNotationHelper(event, request).image_link}
            ${ChordNotationHelper(event, request).image_link}
        </div>
    </div>
% endfor
</div>

<nav class="row">
    <div class="col-lg-12 text-center">
        <ul class="pagination">
            ${paginator.pager(
                '$link_first $link_previous ~3~ $link_next $link_last', 
                show_if_single_page=True,
                )}
        </ul>
    </nav>
</nav>
% else:
<div>
    <h1>Nothing found.</h1>
    <h2>Insert coin to try again.</h2>
</div>
% endif
</div>