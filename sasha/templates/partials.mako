<%!
    from pyramid.url import route_url, current_route_url
    from sasha import domaintools
    from sasha.tools.assettools.ChordNotation import ChordNotation
    from sasha.tools.assettools.FingeringNotation import FingeringNotation
    from sasha.tools.assettools.MP3Audio import MP3Audio
%>

<%def name="event_grid_item(event, instrument)">
    <div id="${event.canonical_event_name}" class="col-sm-3 col-xs-6">
        <a class="btn btn-default btn-block btn-sm" 
            href="${event.get_url(request)}" 
            >${event.get_link_text().decode('utf-8')}</a>
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
    <div class="form-group">
        <div class="input-group">
            <span class="input-group-addon">With pitches</span>
            <input type="text" class="form-control" 
                name="with_pitches" id="with-pitches"
                placeholder="i.e. eqs4 ef6 gs5" value="${with_pitches}"/>
            <span class="input-group-addon">?</span>
        </div>
    </div>
</%def>

<%def name="search_form_group_without_pitches(without_pitches)">
    <div class="form-group">
        <div class="input-group">
            <span class="input-group-addon">Without pitches</span>
            <input type="text" class="form-control" 
                name="without_pitches" id="without-pitches"
                placeholder="i.e. c4 ef6 gs5" value="${without_pitches}"/>
            <span class="input-group-addon">?</span>
        </div>
    </div>
</%def>

<%def name="search_form_group_with_pitch_classes(with_pitch_classes)">
    <div class="form-group">
        <div class="input-group">
            <span class="input-group-addon">With pitch-classes</span>
            <input type="text" class="form-control" 
                name="with_pitch_classes" id="with-pitch-classes"
                placeholder="i.e. cs e gqf" value="${with_pitch_classes}"/>
            <span class="input-group-addon">?</span>
        </div>
    </div>
</%def>

<%def name="search_form_group_without_pitch_classes(without_pitch_classes)">
    <div class="form-group">
        <div class="input-group">
            <span class="input-group-addon">Without pitch-classes</span>
            <input type="text" class="form-control" 
                name="without_pitch_classes" id="without-pitch-classes"
                placeholder="i.e. dqf f bf" value="${without_pitch_classes}"/>
            <span class="input-group-addon">?</span>
        </div>
    </div>
</%def>

<%def name="search_form_group_with_keys(with_keys)">
    <div class="form-group">
        <div class="input-group">
            <span class="input-group-addon">With keys</span>
            <input type="text" class="form-control" 
                name="with_keys" id="with-keys"
                placeholder="i.e. 8va X Bis" value="${with_keys}"/>
            <span class="input-group-addon">?</span>
        </div>
    </div>
</%def>

<%def name="search_form_group_without_keys(without_keys)">
    <div class="form-group">
        <div class="input-group">
            <span class="input-group-addon">Without keys</span>
            <input type="text" class="form-control" 
                name="without_keys" id="without-keys"
                placeholder="i.e. L1 R1 C3" value="${without_keys}"/>
            <span class="input-group-addon">?</span>
        </div>
    </div>
</%def>

<%def name="cluster_listing(current_cluster, all_clusters, feature_name, feature_title)">
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
                href="${cluster.get_url(request)}">
                ${cluster.short_link_text.decode('utf-8')}
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
            % for instrument in domaintools.Instrument.with_events():
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