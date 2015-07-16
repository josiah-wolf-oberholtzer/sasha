<%!
    from pyramid.url import route_url, current_route_url
    from sasha.tools import modeltools
    from sasha.tools.assettools.ChordNotation import ChordNotation
    from sasha.tools.assettools.FingeringNotation import FingeringNotation
    from sasha.tools.assettools.MP3Audio import MP3Audio
%>

<%def name="event_grid_item(event, instrument)">
    <div id="${event.canonical_event_name}" class="col-sm-3 col-xs-6 event-grid">
        <a class="btn btn-default btn-block btn-sm" 
            href="${event.get_url(request)}" 
            >${event.link_text.decode('utf-8')}</a>
        <a class="btn btn-default btn-block btn-sm" 
            href="${instrument.get_url(request)}" 
            >${instrument.name}</a>
        ${MP3Audio(event).get_audio_tag(request)}
        <div class="text-center event-image">
            ${FingeringNotation(event).get_image_link(request)}
            ${ChordNotation(event).get_image_link(request)}
        </div>
    </div>
</%def>

<%def name="pagination(paginator)">
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
</%def>

<%def name="search_form_group_with_pitches(with_pitches)">
    <%
    with_pitches = ' '.join(
        '{}{}'.format(x.pitch_class_name, x.octave_number)
        for x in with_pitches
        )
    %>
    <div class="form-group">
        <div class="input-group">
            <span class="input-group-addon">With pitches</span>
            <input type="text" class="form-control" 
                name="with_pitches" id="with-pitches"
                placeholder="i.e. eqs4 ef6 gs5" value="${with_pitches}"/>
            <span class="input-group-addon" data-toggle="modal" data-target="#modal-info-pitches">?</span>
        </div>
    </div>
</%def>

<%def name="search_form_group_without_pitches(without_pitches)">
    <%
    without_pitches = ' '.join(
        '{}{}'.format(x.pitch_class_name, x.octave_number)
        for x in without_pitches
        )
    %>
    <div class="form-group">
        <div class="input-group">
            <span class="input-group-addon">Without pitches</span>
            <input type="text" class="form-control" 
                name="without_pitches" id="without-pitches"
                placeholder="i.e. c4 ef6 gs5" value="${without_pitches}"/>
            <span class="input-group-addon" data-toggle="modal" data-target="#modal-info-pitches">?</span>
        </div>
    </div>
</%def>

<%def name="search_form_group_with_pitch_classes(with_pitch_classes)">
    <%
    with_pitch_classes = ' '.join(str(x) for x in with_pitch_classes)
    %>
    <div class="form-group">
        <div class="input-group">
            <span class="input-group-addon">With pitch-classes</span>
            <input type="text" class="form-control" 
                name="with_pitch_classes" id="with-pitch-classes"
                placeholder="i.e. cs e gqf" value="${with_pitch_classes}"/>
            <span class="input-group-addon" data-toggle="modal" data-target="#modal-info-pitch-classes">?</span>
        </div>
    </div>
</%def>

<%def name="search_form_group_without_pitch_classes(without_pitch_classes)">
    <%
    without_pitch_classes = ' '.join(str(x) for x in without_pitch_classes)
    %>
    <div class="form-group">
        <div class="input-group">
            <span class="input-group-addon">Without pitch-classes</span>
            <input type="text" class="form-control" 
                name="without_pitch_classes" id="without-pitch-classes"
                placeholder="i.e. dqf f bf" value="${without_pitch_classes}"/>
            <span class="input-group-addon" data-toggle="modal" data-target="#modal-info-pitch-classes">?</span>
        </div>
    </div>
</%def>

<%def name="search_form_group_with_keys(with_keys)">
    <%
    with_keys = ' '.join(x for x in sorted(with_keys))
    %>
    <div class="form-group">
        <div class="input-group">
            <span class="input-group-addon">With keys</span>
            <input type="text" class="form-control" 
                name="with_keys" id="with-keys"
                placeholder="i.e. 8va X Bis" value="${with_keys}"/>
            <span class="input-group-addon" data-toggle="modal" data-target="#modal-info-keys">?</span>
        </div>
    </div>
</%def>

<%def name="search_form_group_without_keys(without_keys)">
    <%
    without_keys = ' '.join(x for x in sorted(without_keys))
    %>
    <div class="form-group">
        <div class="input-group">
            <span class="input-group-addon">Without keys</span>
            <input type="text" class="form-control" 
                name="without_keys" id="without-keys"
                placeholder="i.e. L1 R1 C3" value="${without_keys}"/>
            <span class="input-group-addon" data-toggle="modal" data-target="#modal-info-keys">?</span>
        </div>
    </div>
</%def>

<%def name="search_form_modal_info_pitches()">
<div id="modal-info-pitches" class="modal fade" tabindex="-1" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">Pitches</h4>
      </div>
      <div class="modal-body">

        <p>Pitch are indicated by the combination of a diatonic pitch
        name, an optional alteration, and an octave number.</p>

        <blockquote>
            <p><strong>d</strong> + <strong>qs</strong> + <strong>5</strong> =
            <strong>dqs5</strong></p>
            <p>(D quarter-sharp in the octave above middle-C's octave)</p>
        </blockquote>

        <p>The following diatonic pitch names are permitted:
        <strong>c</strong>, <strong>d</strong>, <strong>e</strong>,
        <strong>f</strong>, <strong>g</strong>, <strong>a</strong>, and
        <strong>b</strong>.</p>
        
        <p>Alterations indicate whether the pitch-class is sharp or flat, and
        to what degree. The following alterations are permitted:
        <strong>s</strong> (sharp), <strong>ss</strong> (double-sharp),
        <strong>f</strong> (flat), <strong>ff</strong> (double-flat),
        <strong>qs</strong> (quarter-sharp), <strong>tqs</strong>
        (three-quarter-sharp), <strong>qf</strong> (quarter-flat), and
        <strong>tqf</strong> (three-quarter-flat).

        <p>Octave numbers treat the octave starting on middle-C as
        <strong>4</strong>.</p>

      </div>
    </div>
  </div>
</div>
</%def>

<%def name="search_form_modal_info_pitch_classes()">
<div id="modal-info-pitch-classes" class="modal fade" tabindex="-1" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">Pitch-classes</h4>
      </div>
      <div class="modal-body">

        <p>Pitch-classes are the set of all pitches that are a whole number of
        octaves apart - all Cs, all Ds, etc.</p>

        <p>Pitch-classes are indicated by the combination of a diatonic pitch
        name and an optional alteration.</p>

        <blockquote>
            <p><strong>d</strong> + <strong>qs</strong> = <strong>dqs</strong></p>
            <p>(D quarter-sharp)</p>

        </blockquote>

        <p>The following diatonic pitch names are permitted:
        <strong>c</strong>, <strong>d</strong>, <strong>e</strong>,
        <strong>f</strong>, <strong>g</strong>, <strong>a</strong>, and
        <strong>b</strong>.</p>
        
        <p>Alterations indicate whether the pitch-class is sharp or flat, and
        to what degree. The following alterations are permitted:
        <strong>s</strong> (sharp), <strong>ss</strong> (double-sharp),
        <strong>f</strong> (flat), <strong>ff</strong> (double-flat),
        <strong>qs</strong> (quarter-sharp), <strong>tqs</strong>
        (three-quarter-sharp), <strong>qf</strong> (quarter-flat), and
        <strong>tqf</strong> (three-quarter-flat).

      </div>
    </div>
  </div>
</div>
</%def>

<%def name="search_form_modal_info_keys(instrument)">
<div id="modal-info-keys" class="modal fade" tabindex="-1" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">Instrument Key Names</h4>
      </div>
      <div class="modal-body">

        <p>
        The following ${instrument.get_link(request)} key names are
        permitted:
        % for key_name in instrument.key_names[:-1]:
        <strong>${key_name}</strong>,
        % endfor
        and <strong>${instrument.key_names[-1]}</strong>.
        </p>

      </div>
    </div>
  </div>
</div>
</%def>

<%def name="search_form_modal_info_order_by()">
<div id="modal-info-order-by" class="modal fade" tabindex="-1" role="dialog">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span></button>
        <h4 class="modal-title">Event Sorting</h4>
      </div>
      <div class="modal-body">

        <p>SASHA provides a variety of sorting methods on its multiphonic
        collection.</p>

        <p>Consult the <a href="/help/">documentation</a> for further
        discussion.</p>

        <dl class="dl-horizontal">

          <dt>MD5 Hash</dt><dd>A unique identifier for the audio content of
          the multiphonic's recording. Does not indicate any spectral
          information.</dd>

          <dt>Log Harmonicity</dt><dd>A measure of the periodicity of the
          signal. A lower harmonicity indicates a noisier signal.</dd>

          <dt>Spectral Centroid</dt><dd>A measure of the frequency
          "center-of-mass". A lower centroid indicates a darker sound, while a
          higher centroid indicates a higher or brighter sound.</dd>

          <dt>Spectral Crest</dt><dd>A ratio of the power of the spectral peaks
          to the average power of the signal.</dd>

          <dt>Spectral Flatness</dt><dd>The degree to which all frequencies in
          the signal have the same power. Higher flatness indicates noisiness
          while lower flatness indicates a more pure, sinusoidal tone.<dd>

          <dt>Spectral Kurtosis</dt><dd>A measure of the peakiness of the
          spectrum.</dd>

          <dt>Spectral Rolloff</dt><dd>The frequency at which 85% of the power
          is contained in lower frequencies.</dd>

          <dt>Spectral Skewness</dt><dd>A measure of the asymmetry of the
          spectrum.</dd>

          <dt>Spectral Spread</dt><dd>A measure of the band-width of the
          spectrum around its centroid.</dd>

        </dl>
      </div>
    </div>
  </div>
</div>
</%def>

<%def name="search_form_group_order_by(order_by)">
    <div class="form-group">
        <div class="input-group">
            <span class="input-group-addon">Order by</span>
            <select class="form-control" name="order_by">
                <option ${'selected' if order_by == 'md5' else ''} value="md5">MD5 Hash</option>
                <option ${'selected' if order_by == 'log_harmonicity' else ''} value="log_harmonicity">Log Harmonicity</option>
                <option ${'selected' if order_by == 'spectral_centroid' else ''} value="spectral_centroid">Spectral Centroid</option>
                <option ${'selected' if order_by == 'spectral_crest' else ''} value="spectral_crest">Spectral Crest</option>
                <option ${'selected' if order_by == 'spectral_flatness' else ''} value="spectral_flatness">Spectral Flatness</option>
                <option ${'selected' if order_by == 'spectral_kurtosis' else ''} value="spectral_kurtosis">Spectral Kurtosis</option>
                <option ${'selected' if order_by == 'spectral_rolloff' else ''} value="spectral_rolloff">Spectral Rolloff</option>
                <option ${'selected' if order_by == 'spectral_skewness' else ''} value="spectral_skewness">Spectral Skewness</option>
                <option ${'selected' if order_by == 'spectral_spread' else ''} value="spectral_spread">Spectral Spread</option>
            </select>
            <span class="input-group-addon" data-toggle="modal" data-target="#modal-info-order-by">?</span>
        </div>
    </div>
</%def>

<%def name="cluster_listing(current_instrument, current_cluster, all_clusters, feature_name, feature_title)">
<%
    instrument_name = current_instrument.snake_case_name if current_instrument is not None else ''
%>
<div class="form-group">
    <label class="col-sm-3 control-label">${feature_title} Clusters</label>
    <div class="col-sm-9">
        <div class="btn-group btn-group-justified" role="group">
        % for cluster in all_clusters[feature_name]:
            % if current_cluster.id == cluster.id:
            <a class="btn btn-default active"
            % else:
            <a class="btn btn-default"
            % endif
                href="${request.route_url(
                    'cluster',
                    feature=cluster.feature,
                    cluster_id=cluster.cluster_id,
                    _query={'instrument': instrument_name},
                    )
                    }">${cluster.short_link_text.decode('utf-8')}</a>
            </a>
        % endfor
        </div>       
    </div>
</div>
</%def>

<%def name="instrument_listing(current_instrument, all_instruments)">
<div class="form-group">
    <label class="col-sm-3 control-label">Instruments</label>
    <div class="col-sm-9">
        <div class="btn-group btn-group-justified" role="group">
            % if current_instrument is None:
            <a class="btn btn-default active"
            % else:
            <a class="btn btn-default"
            % endif
                href="${current_route_url(request, _query={'instrument': ''})}"
                >All Instruments</a>
            % for instrument in modeltools.Instrument.with_events():
                % if current_instrument is not None and instrument.id == current_instrument.id:
                <a class="btn btn-default active" 
                % else:
                <a class="btn btn-default" 
                % endif
                    href="${current_route_url(request, _query={'instrument': 
                        instrument.snake_case_name
                        })}">${instrument.name}</a>
            % endfor
        </div>
    </div>
</div>
</%def>