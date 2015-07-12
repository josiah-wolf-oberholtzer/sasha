<%inherit file="sasha:templates/search.mako"/>

<%!
    from sasha.tools.assettools import FingeringNotation
    from sasha.tools.modeltools import Event
%>

<%block name="other">
<div class="grid_12 section_title">Top 12 Similar ${instrument.get_link(request)} Fingerings</div>
<div class="events clearfix">
%for similar_fingering in fingerings:
    <% event = Event.objects(fingering=similar_fingering).first() %>
    <div class="event grid_1">
        <div class="annotation
        notations">${FingeringNotation(event).get_image_link(request)}</div>
    </div>
%endfor
</div>
</%block>