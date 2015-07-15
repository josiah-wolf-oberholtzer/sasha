<%inherit file="sasha:templates/search.mako"/>

<%namespace file="sasha:templates/partials.mako" name="partials"/>

<%!
    from sasha import modeltools
%>

<%block name="searchbar">
<div class="jumbotron">
    <div class="container">
        <h2>Explore multiphonic clusters</h2>
        <p><em>Cluster analysis</em> groups multiphonics together into <em>clusters</em>
        according to the similarity of the spectral features.</p>
    </div>
</div>

<form class="form-horizontal">
    ${partials.instrument_listing(current_instrument, modeltools.Instrument.with_events())}
    ${partials.cluster_listing(current_instrument, current_cluster, all_clusters, 'chroma', 'Chroma')}
    ${partials.cluster_listing(current_instrument, current_cluster, all_clusters, 'constant_q', 'Constant-Q')}
    ${partials.cluster_listing(current_instrument, current_cluster, all_clusters, 'mfcc', 'MFCC')}
</form>
</%block>