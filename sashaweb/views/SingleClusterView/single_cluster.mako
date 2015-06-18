<%inherit file="sashaweb:views/SearchView/search.mako"/>

<%namespace file="sashaweb:templates/partials.mako" name="partials"/>

<%!
    from sasha import domaintools
    from sashaweb import helpers
%>

<%block name="searchbar">
<form class="form-horizontal">
    ${partials.instrument_listing(instrument, domaintools.Instrument.with_events())}
    ${partials.cluster_listing(current_cluster, all_clusters, 'chroma', 'Chroma')}
    ${partials.cluster_listing(current_cluster, all_clusters, 'constant_q', 'Constant-Q')}
    ${partials.cluster_listing(current_cluster, all_clusters, 'mfcc', 'MFCC')}
</form>
</%block>