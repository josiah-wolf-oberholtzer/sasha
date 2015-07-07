<%inherit file="sashaweb:templates/base.mako"/>

<%namespace file="sashaweb:templates/partials.mako" name="partials" />

<%!
    from sasha import sasha_configuration
    from sasha.tools.domaintools import Event
    from sasha.tools.domaintools import Instrument
    from sashaweb.helpers.ChordNotationHelper import ChordNotationHelper
    from sashaweb.helpers.ChromaNotationHelper import ChromaNotationHelper
    from sashaweb.helpers.MP3AudioHelper import MP3AudioHelper
    from sashaweb.helpers.FingeringNotationHelper import FingeringNotationHelper
    from sashaweb.helpers.PartialTrackingPlotHelper import PartialTrackingPlotHelper
%>

<div class="page-header">
<h2>
${current_instrument.get_link(request)}
|
${current_event.get_numbered_link(request)}
</h2>
</div>

<div class="row">
<dl class="col-sm-6">
    <dt>Instrument</dt>
    <dd><p>${current_instrument.get_link(request)}</p></dd>

    <dt>Event &numero;</dt>
    <dd><p>${current_event.get_numbered_link(request)}</p></dd>

    <dt>Audio MD5 hash</dt>
    <dd><p>${current_event.get_md5_link(request)}</p></dd>

    <dt>Key names</dt>
    <dd><p>${current_event.fingering.get_link(request)}</p></dd>

    <dt>Clusters</dt>
    <dd><p>
    %for i, cluster in enumerate(clusters):
        %if 0 < i:
        | 
        %endif
        ${cluster.get_long_link(request)}
    %endfor
    </p></dd>
</dl>
<dl class="col-sm-3">
    <dt><p>Chord notation</p></dt>
    <dd><p>${ChordNotationHelper(current_event, request).image_link}</p></dd>
</dl>
<dl class="col-sm-3">
    <dt><p>Fingering notation</p></dt>
    <dd><p>${FingeringNotationHelper(current_event, request).image_link}</p></dd>
</dl>
</div>

<dl>
    <dt>Audio</dt>
    <dd class="text-center"><p>${MP3AudioHelper(current_event, request).audio}</p></dd>
    <dt><p>Chroma notation</p></dt>
    <dd class="text-center"><p>${ChromaNotationHelper(current_event, request).image_link}</p></dd>
    <dt><p>Partial tracking analysis</p></dt>
    <dd class="text-center"><p>${PartialTrackingPlotHelper(current_event, request).image_link}</p></dd>
</dl>


% if len(chroma_events):
<div class="page-header">
    <h2><small>
        Top ${len(chroma_events)}
        Similar ${current_instrument.get_link(request)} Recordings via
        <a href="http://www.omras2.org/audioDB">AudioDB</a>
        <a href="http://en.wikipedia.org/wiki/Pitch_class">Chroma</a> Matching
    </small></h2>
</div>
<div class="row">
% for i, event in enumerate(chroma_events):
    % if 0 < i and i % 4 == 0:
    </div>
    <div class="row event-row">
    % endif
    ${partials.event_grid_item(event, Instrument.get_one(id=event.instrument_id))}
% endfor
</div>
% endif

% if len(mfcc_events):
<div class="page-header">
    <h2><small>
        Top ${len(mfcc_events)}
        Similar ${current_instrument.get_link(request)} Recordings via 
        <a href="http://www.omras2.org/audioDB">AudioDB</a>
        <a href="http://en.wikipedia.org/wiki/Mel-frequency_cepstrum">MFCC</a> Matching
    </small></h2>
</div>
<div class="row">
% for i, event in enumerate(mfcc_events):
    % if 0 < i and i % 4 == 0:
    </div>
    <div class="row event-row">
    % endif
    ${partials.event_grid_item(event, Instrument.get_one(id=event.instrument_id))}
% endfor
</div>
% endif

<div class="page-header">
    <h2><small>
        Top 12 Similar ${current_instrument.get_link(request)}
        Fingerings
    </small></h2>
</div>

<div class="row">
% for fingering in fingerings:
<div class="col-xs-1 text-center">
    <div class="annotation notations">${FingeringNotationHelper(fingering, request).image_link}</div>
</div>
% endfor
</div>