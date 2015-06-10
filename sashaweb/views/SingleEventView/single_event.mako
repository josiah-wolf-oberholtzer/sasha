<%inherit file="sashaweb:templates/base__search.mako"/>

<%!
    from sasha import sasha_configuration, Event, Instrument
    from sashaweb.helpers import EventHelper, FingeringHelper, InstrumentHelper, ClusterHelper
    from sashaweb.helpers import ChordNotationHelper, ChromaNotationHelper, MP3AudioHelper
    from sashaweb.helpers import FingeringNotationHelper, PartialTrackingPlotHelper
%>

<div id="page_title" class="grid_12">${InstrumentHelper(single_event, request).link} Event: ${single_event.md5}</div>

<div id="single_event" class="clearfix">

    <div class="grid_1 push_1">&nbsp;</div>
    <div class="grid_1 event_data">
        <div class="label">ID</div>
        <div class="datum">${EventHelper(single_event, request).numbered_link}</div>
    </div>
    <div class="grid_4 event_data">
        <div class="label">AUDIO MD5 FINGERPRINT</div>
        <div class="datum">${EventHelper(single_event, request).md5_link}</div>
    </div>
    <div class="grid_3 event_data">
        <div class="label">INSTRUMENT</div>
        <div class="datum">${InstrumentHelper(single_event, request).link}</div>
    </div>
    <div class="grid_2 event_data">
        <div class="label">KEY NAMES</div>
        <div class="datum">${FingeringHelper(single_event, request).link}</div>
    </div>

    <div class="clearfix"></div>

    <div class="grid_1 push_1">&nbsp;</div>

    <div class="grid_2 event_data">
        <div class="bottom">
            <div class="label">AUDIO</div>
            <div class="datum">${MP3AudioHelper(single_event, request).audio}</div>
        </div>

        <div class="label">CLUSTERS</div>
        %for cluster in clusters:
        <div class="datum">${ClusterHelper(cluster, request).verbose_link}</div>
        %endfor
    </div>

    <div class="event_data grid_1">
        <div class="label">KEYS</div>
        <div class="datum">${FingeringNotationHelper(single_event, request).image_link}</div>
    </div>
    <div class="event_data grid_2">
        <div class="label">CHORD</div>
        <div class="datum">${ChordNotationHelper(single_event, request).image_link}</div>
    </div>
    <div class="event_data grid_5">
        <div class="label">CHROMA MEAN and STD/DEV ANALYSIS</div>
        <div class="datum">${ChromaNotationHelper(single_event, request).image_link}</div>
    </div>

    <div class="clearfix"></div>

    <div class="grid_1">&nbsp;</div>
    <div class="event_data grid_10">
        <div class="label">PARTIAL TRACKING ANALYSIS</div>
        <div class="datum" class="push_1">${PartialTrackingPlotHelper(single_event, request).image_link}</div>
    </div>

</div>

<div class="divider grid_12 clearfix"></div>

<div class="grid_12 section_title">Top ${len(chroma_events)}
    Similar ${InstrumentHelper(single_event, request).link} Recordings via
    <a href="http://www.omras2.org/audioDB">AudioDB</a>
    <a href="http://en.wikipedia.org/wiki/Pitch_class">Chroma</a> Matching
</div>

<div class="events clearfix">
%for i, event in enumerate(chroma_events):
    % if i % 6 == 0 and 0 < i:
    <div class="clearfix grid_12 divider"></div>
    % endif
    <div id="${event.canonical_name}" class="event grid_2">
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

<div class="clearfix grid_12 divider"></div>

<div class="grid_12 section_title">Top ${len(mfcc_events)}
    Similar ${InstrumentHelper(single_event, request).link} Recordings via 
    <a href="http://www.omras2.org/audioDB">AudioDB</a>
    <a href="http://en.wikipedia.org/wiki/Mel-frequency_cepstrum">MFCC</a> Matching
</div>

<div class="events clearfix">
%for i, event in enumerate(mfcc_events):
    % if i % 6 == 0 and 0 < i:
    <div class="clearfix grid_12 divider"></div>
    % endif
    <div id="${event.canonical_name}" class="event grid_2">
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

<div class="clearfix grid_12 divider"></div>

<div class="grid_12 section_title">Top 12 Similar ${InstrumentHelper(single_event, request).link} Fingerings</div>

<div class="events clearfix">
%for f in fingerings:
    <div id="${event.canonical_name}" class="event grid_1">
        <div class="annotation notations">${FingeringNotationHelper(f, request).image_link}</div>
    </div>
%endfor
</div>

<div class="clearfix grid_12 divider"></div>
