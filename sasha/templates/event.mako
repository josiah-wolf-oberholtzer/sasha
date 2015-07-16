<%inherit file="sasha:templates/base.mako"/>

<%namespace file="sasha:templates/partials.mako" name="partials" />

<%!
    from sasha import sasha_configuration
    from sasha.tools.modeltools import Event
    from sasha.tools.assettools.ArpeggioNotation import ArpeggioNotation
    from sasha.tools.assettools.ChordNotation import ChordNotation
    from sasha.tools.assettools.ChromaNotation import ChromaNotation
    from sasha.tools.assettools.MP3Audio import MP3Audio
    from sasha.tools.assettools.FingeringNotation import FingeringNotation
    from sasha.tools.assettools.PartialTrackingPlot import PartialTrackingPlot
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
    <dt>
      <p>Instrument</p>
    </dt>
    <dd><p>${current_instrument.get_link(request)}</p></dd>

    <dt>
      <p>Event &numero;</p>
    </dt>
    <dd><p>${current_event.get_numbered_link(request)}</p></dd>

    <dt data-toggle="modal" data-target="#modal-info-md5">
      <p>Audio MD5 Hash <span class="badge">?</span></p>
    </dt>
    <dd><p>${current_event.get_md5_link(request)}</p></dd>

<div id="modal-info-md5" class="modal fade" tabindex="-1" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">MD5 Hash</h4>
      </div>
      <div class="modal-body">
        Info
      </div>
    </div>
  </div>
</div>

    <dt data-toggle="modal" data-target="#modal-info-key-names">
      <p>Key Names <span class="badge">?</span></p>
    </dt>
    <dd><p>${current_event.fingering.get_link(request)}</p></dd>

<div id="modal-info-key-names" class="modal fade" tabindex="-1" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">Key Names</h4>
      </div>
      <div class="modal-body">
        Info
      </div>
    </div>
  </div>
</div>

    <dt data-toggle="modal" data-target="#modal-info-clusters">
      <p>Clusters <span class="badge">?</span></p>
    </dt>
    <dd><p>
    %for i, cluster in enumerate(clusters):
        %if 0 < i:
        | 
        %endif
        ${cluster.get_long_link(request)}
    %endfor
    </p></dd>

<div id="modal-info-clusters" class="modal fade" tabindex="-1" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">Clusters</h4>
      </div>
      <div class="modal-body">
        Info
      </div>
    </div>
  </div>
</div>

</dl>
<dl class="col-sm-6">

    <dt data-toggle="modal" data-target="#modal-info-arpeggio-notation">
      <p>Arpeggio Notation <span class="badge">?</span></p>
    </dt>
    <dd><p>${ArpeggioNotation(current_event).get_image_link(request)}</p></dd>

<div id="modal-info-arpeggio-notation" class="modal fade" tabindex="-1" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">Arpeggio Notation</h4>
      </div>
      <div class="modal-body">
        Info
      </div>
    </div>
  </div>
</div>

    <dt>
      <p>Fingering notation</p>
    </dt>
    <dd><p>${FingeringNotation(current_event).get_image_link(request)}</p></dd>

</dl>
</div>

<dl>

    <dt>
      <p>Audio</p>
    </dt>
    <dd class="text-center"><p>${MP3Audio(current_event).get_audio_tag(request)}</p></dd>

    <dt data-toggle="modal" data-target="#modal-info-chroma-notation">
      <p>Chroma notation <span class="badge">?</span></p>
    </dt>
    <dd class="text-center"><p>${ChromaNotation(current_event).get_image_link(request)}</p></dd>

<div id="modal-info-chroma-notation" class="modal fade" tabindex="-1" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">Chroma Notation</h4>
      </div>
      <div class="modal-body">
        Info
      </div>
    </div>
  </div>
</div>

    <dt data-toggle="modal" data-target="#modal-info-partial-tracking-plot">
      <p>Partial tracking analysis <span class="badge">?</span></p>
    </dt>
    <dd class="text-center"><p>${PartialTrackingPlot(current_event).get_image_link(request)}</p></dd>

<div id="modal-info-partial-tracking-plot" class="modal fade" tabindex="-1" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">Partial Tracking Plot</h4>
      </div>
      <div class="modal-body">
        Info
      </div>
    </div>
  </div>
</div>

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
    ${partials.event_grid_item(event, event.fingering.instrument)}
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
    ${partials.event_grid_item(event, event.fingering.instrument)}
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
    <% event = Event.objects(fingering=fingering).first() %>
    <div class="annotation notations">${FingeringNotation(event).get_image_link(request)}</div>
</div>
% endfor
</div>