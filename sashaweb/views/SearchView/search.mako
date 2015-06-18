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
<div class="row">
    <div class="jumbotron col-sm-6">
        <h2>Search</h2>
        <p>Add constraints to find new multiphonics.</p>
    </div>
    <form action="${search_action}" method="get" class="col-sm-6">
        <div class="form-group">
                <div class="input-group">
                    <span class="input-group-addon">With pitches</span>
                    <input type="text" class="form-control" 
                        name="with_pitches" id="with-pitches"
                        placeholder="i.e. eqs4 ef6 gs5" value="${with_pitches}"/>
                    <span class="input-group-addon">?</span>
                </div>
        </div>
        <div class="form-group">
                <div class="input-group">
                    <span class="input-group-addon">Without pitches</span>
                    <input type="text" class="form-control" 
                        name="without_pitches" id="without-pitches"
                        placeholder="i.e. c4 ef6 gs5" value="${without_pitches}"/>
                    <span class="input-group-addon">?</span>
                </div>
        </div>
        <div class="form-group">
                <div class="input-group">
                    <span class="input-group-addon">With pitch-classes</span>
                    <input type="text" class="form-control" 
                        name="with_pitch_classes" id="with-pitch-classes"
                        placeholder="i.e. cs e gqf" value="${with_pitch_classes}"/>
                    <span class="input-group-addon">?</span>
                </div>
        </div>
        <div class="form-group">
                <div class="input-group">
                    <span class="input-group-addon">Without pitch-classes</span>
                    <input type="text" class="form-control" 
                        name="without_pitch_classes" id="without-pitch-classes"
                        placeholder="i.e. dqf f bf" value="${without_pitch_classes}"/>
                    <span class="input-group-addon">?</span>
                </div>
        </div>
        <div class="form-group">
            <button type="submit" class="btn btn-default">Search</button>
        </div>
    </form>
</div>
</%block>

<%block name="searchresults">
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
    <div class="row event-row">
    % endif
    <div id="${event.canonical_name}" class="col-sm-3 col-xs-6">
        <a class="btn btn-default btn-block btn-sm" 
            href="${EventHelper(event, request).url}" 
            >${EventHelper(event, request).link_text.decode('utf-8')}</a>
        <a class="btn btn-default btn-block btn-sm" 
            href="${InstrumentHelper(event, request).url}" 
            >${InstrumentHelper(event, request).name}</a>
        ${MP3AudioHelper(event, request).audio}
        <div class="text-center event-image">
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
</%block>

</div>