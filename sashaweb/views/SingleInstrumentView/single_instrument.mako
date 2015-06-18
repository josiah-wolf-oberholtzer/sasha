<%inherit file="sashaweb:views/SearchView/search.mako"/>

<%namespace file="sashaweb:templates/partials.mako" name="partials" />

<%!
    from sashaweb import helpers
%>

<%block name="searchbar">
<div class="row">
    <div class="jumbotron col-sm-6">
        <h2>Explore
            ${helpers.InstrumentHelper(instrument, request).link}
            multiphonics
            </h2>
        <p>Add constraints to find new multiphonics for this instrument.</p>
    </div>
    <form action="${search_action}" method="get" class="col-sm-6">
        ${partials.search_form_group_with_keys(with_keys)}
        ${partials.search_form_group_without_keys(without_keys)}
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