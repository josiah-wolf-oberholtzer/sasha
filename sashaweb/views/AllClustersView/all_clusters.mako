<%inherit file="sashaweb:templates/base.mako"/>

<%!
    from sashaweb.helpers import ClusterHelper
%>

<%block name="title">
<div id="title" class="grid_12">All Clusters</div>
</%block>

<div class="grid_6 push_3 bottom clusters">
    <div class="section_title">CHROMA Clusters</div>
    <ul>
% for cluster in clusters['chroma']:
        <li>${ClusterHelper(cluster, request).link}</li>
% endfor
    </ul>
</div>

<div class="clear"></div>
<div class="grid_6 push_3 divider"></div>
<div class="clear"></div>

<div class="grid_6 push_3 bottom clusters">
    <div class="section_title">Constant-Q Clusters</div>
    <ul>
% for cluster in clusters['constant_q']:
        <li>${ClusterHelper(cluster, request).link}</li>
% endfor
    </ul>
</div>

<div class="clear"></div>
<div class="grid_6 push_3 divider"></div>
<div class="clear"></div>

<div class="grid_6 push_3 bottom clusters">
    <div class="section_title">MFCC Clusters</div>
    <ul>
% for cluster in clusters['mfcc']:
        <li>${ClusterHelper(cluster, request).link}</li>
% endfor
    </ul>
</div>

<div class="clear"></div>
<div class="grid_6 push_3 divider"></div>
<div class="clear"></div>
