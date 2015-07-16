<%inherit file="sasha:templates/search.mako"/>

<%namespace file="sasha:templates/partials.mako" name="partials" />

<%block name="searchbar">
<div class="row">
    <div class="col-sm-6">
        <div class="jumbotron">
            <div class="container">
                <h2>Explore
                    ${instrument.get_link(request)}
                    multiphonics
                    </h2>
                <p>Add constraints to find new multiphonics for this instrument.</p>
            </div>
        </div>
    </div>
    <form action="${search_action}" method="get" class="col-sm-6">
        ${partials.search_form_modal_info_pitches()}
        ${partials.search_form_modal_info_pitch_classes()}
        ${partials.search_form_modal_info_keys(instrument)}
        ${partials.search_form_modal_info_order_by()}
        ${partials.search_form_group_with_keys(
            search_parameters['with_keys'])}
        ${partials.search_form_group_without_keys(
            search_parameters['without_keys'])}
        ${partials.search_form_group_with_pitches(
            search_parameters['with_pitches'])}
        ${partials.search_form_group_without_pitches(
            search_parameters['without_pitches'])}
        ${partials.search_form_group_with_pitch_classes(
            search_parameters['with_pitch_classes'])}
        ${partials.search_form_group_without_pitch_classes(
            search_parameters['without_pitch_classes'])}
        ${partials.search_form_group_order_by(layout_parameters['order_by'])}
        <div class="form-group">
            <button type="submit" class="btn btn-default">Search</button>
        </div>
    </form>
</div>
</%block>