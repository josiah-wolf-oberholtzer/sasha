<%inherit file="sashaweb:templates/base.mako"/>

<%namespace file="sashaweb:templates/partials.mako" name="partials" />

<%!
    from sasha import sasha_configuration
    from sasha.tools.domaintools import Event
    from sasha.tools.domaintools import Instrument
    from sashaweb.helpers.EventHelper import EventHelper
    from sashaweb.helpers.FingeringHelper import FingeringHelper
    from sashaweb.helpers.InstrumentHelper import InstrumentHelper
    from sashaweb.helpers.ChordNotationHelper import ChordNotationHelper
    from sashaweb.helpers.ChromaNotationHelper import ChromaNotationHelper
    from sashaweb.helpers.ClusterHelper import ClusterHelper
    from sashaweb.helpers.MP3AudioHelper import MP3AudioHelper
    from sashaweb.helpers.FingeringNotationHelper import FingeringNotationHelper
    from sashaweb.helpers.PartialTrackingPlotHelper import PartialTrackingPlotHelper
%>

<dl>

    <dt>Instrument</dt>
    <dd>${InstrumentHelper(single_event, request).link}</dd>

    <dt>Event &numero;</dt>
    <dd>${EventHelper(single_event, request).numbered_link}</dd>

    <dt>Audio MD5 hash</dt>
    <dd>${EventHelper(single_event, request).md5_link}</dd>

    <dt>Key names</dt>
    <dd>${FingeringHelper(single_event, request).link}</dd>

    <dt>Clusters</dt>
    <dd>
    %for cluster in clusters:
    ${ClusterHelper(cluster, request).verbose_link}
    %endfor
    </dd>

    <dt>Fingering notation</dt>
    <dd>${FingeringNotationHelper(single_event, request).image_link}</dd>

    <dt>Audio</dt>
    <dd>${MP3AudioHelper(single_event, request).audio}</dd>

    <dt>Chroma notation</dt>
    <dd>${ChromaNotationHelper(single_event, request).image_link}</dd>

    <dt>Chord notation</dt>
    <dd>${ChordNotationHelper(single_event, request).image_link}</dd>

    <dt>Partial tracking analysis</dt>
    <dd>${PartialTrackingPlotHelper(single_event, request).image_link}</dd>

</dl>


% if len(chroma_events):
<p>
    Top ${len(chroma_events)}
    Similar ${InstrumentHelper(single_event, request).link} Recordings via
    <a href="http://www.omras2.org/audioDB">AudioDB</a>
    <a href="http://en.wikipedia.org/wiki/Pitch_class">Chroma</a> Matching
</p>
<div class="row">
% for i, event in enumerate(chroma_events):
    % if 0 < i and i % 4 == 0:
    </div>
    <div class="row event-row">
    % endif
    ${partials.event_grid_item(event)}
% endfor
</div>
% endif

% if len(mfcc_events):
<p>
    Top ${len(mfcc_events)}
    Similar ${InstrumentHelper(single_event, request).link} Recordings via 
    <a href="http://www.omras2.org/audioDB">AudioDB</a>
    <a href="http://en.wikipedia.org/wiki/Mel-frequency_cepstrum">MFCC</a> Matching
</p>
<div class="row">
% for i, event in enumerate(mfcc_events):
    % if 0 < i and i % 4 == 0:
    </div>
    <div class="row event-row">
    % endif
    ${partials.event_grid_item(event)}
% endfor
</div>
% endif

<p>
    Top 12 Similar ${InstrumentHelper(single_event, request).link} Fingerings
</p>

<div class="row">
% for fingering in fingerings:
<div id="${fingering.canonical_name}" class="col-xs-1 text-center">
    <div class="annotation notations">${FingeringNotationHelper(fingering, request).image_link}</div>
</div>
% endfor
</div>