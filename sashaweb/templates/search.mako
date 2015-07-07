<%inherit file="sashaweb:templates/base.mako" />

<%namespace file="sashaweb:templates/partials.mako" name="partials" />

<%block name="searchbar">
<div class="row">
    <div class="col-sm-6">
        <div class="jumbotron">
            <div class="container">
                <h2>Search multiphonics</h2>
                <p>Add constraints to find new multiphonics.</p>
            </div>
        </div>
    </div>
    <form action="${search_action}" method="get" class="col-sm-6">
        ${partials.search_form_group_with_pitches(with_pitches)}
        ${partials.search_form_group_without_pitches(without_pitches)}
        ${partials.search_form_group_with_pitch_classes(with_pitch_classes)}
        ${partials.search_form_group_without_pitch_classes(without_pitch_classes)}
        <div class="form-group">
            <button type="submit" class="btn btn-default">Search</button>
        </div>
    </form>
</div>
</%block>

<%block name="searchresults">
% if len(paginator):
    ${partials.pagination(paginator)}
    <div class="row">
    % for i, event in enumerate(paginator):
        % if 0 < i and i % 4 == 0:
        </div>
        <div class="row event-row">
        % endif
        ${partials.event_grid_item(event, event.instrument)}
    % endfor
    </div>
    ${partials.pagination(paginator)}
% else:
    <div>
        <h1>Nothing found.</h1>
        <h2>Insert coin to try again.</h2>
    </div>
% endif
</%block>

</div>