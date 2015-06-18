<%inherit file="sashaweb:views/SearchView/search.mako"/>

<%!
    from sashaweb.helpers import FingeringNotationHelper, InstrumentHelper
%>

<%block name="other">
<div class="grid_12 section_title">Top 12 Similar ${InstrumentHelper(instrument, request).link} Fingerings</div>
<div class="events clearfix">
%for similar_fingering in fingerings:
    <div id="${similar_fingering.canonical_name}" class="event grid_1">
        <div class="annotation notations">${FingeringNotationHelper(similar_fingering, request).image_link}</div>
    </div>
%endfor
</div>
<div class="clearfix grid_12 divider"></div>
</%block>