<%inherit file="sashaweb:views/SearchView/search.mako"/>
<%!
    from sasha import sasha_configuration, Event, Instrument
    from sashaweb.helpers import EventHelper, FingeringHelper, InstrumentHelper
    from sashaweb.helpers import ChordNotationHelper, ChromaNotationHelper, MP3AudioHelper
    from sashaweb.helpers import FingeringNotationHelper, PartialTrackingPlotHelper
%>

<%block name="searchbar">
<div class="row">
    <div class="jumbotron col-sm-6">
        <h2>${InstrumentHelper(instrument, request).link}</h2>
        <p>Add constraints to find new multiphonics.</p>
    </div>
    <form action="${search_action}" method="get" class="col-sm-6">
        <div class="form-group">
                <div class="input-group">
                    <span class="input-group-addon">With keys</span>
                    <input type="text" class="form-control" 
                        name="with_keys" id="with-keys"
                        placeholder="i.e. 8va X Bis" value="${with_keys}"/>
                    <span class="input-group-addon">?</span>
                </div>
        </div>
        <div class="form-group">
                <div class="input-group">
                    <span class="input-group-addon">Without keys</span>
                    <input type="text" class="form-control" 
                        name="without_keys" id="without-keys"
                        placeholder="i.e. L1 R1 C3" value="${without_keys}"/>
                    <span class="input-group-addon">?</span>
                </div>
        </div>
        <div class="form-group">
                <div class="input-group">
                    <span class="input-group-addon">With pitches</span>
                    <input type="text" class="form-control" 
                        name="with_pitches" id="with-pitches"
                        placeholder="i.e. eqs4 ef6 gs5" value="${with_pitches}"/>
                    <span class="input-group-addon">?</span>
                </div>
        </div>
        <div class="form-group">
                <div class="input-group">
                    <span class="input-group-addon">Without pitches</span>
                    <input type="text" class="form-control" 
                        name="without_pitches" id="without-pitches"
                        placeholder="i.e. c4 ef6 gs5" value="${without_pitches}"/>
                    <span class="input-group-addon">?</span>
                </div>
        </div>
        <div class="form-group">
                <div class="input-group">
                    <span class="input-group-addon">With pitch-classes</span>
                    <input type="text" class="form-control" 
                        name="with_pitch_classes" id="with-pitch-classes"
                        placeholder="i.e. cs e gqf" value="${with_pitch_classes}"/>
                    <span class="input-group-addon">?</span>
                </div>
        </div>
        <div class="form-group">
                <div class="input-group">
                    <span class="input-group-addon">Without pitch-classes</span>
                    <input type="text" class="form-control" 
                        name="without_pitch_classes" id="without-pitch-classes"
                        placeholder="i.e. dqf f bf" value="${without_pitch_classes}"/>
                    <span class="input-group-addon">?</span>
                </div>
        </div>
        <div class="form-group">
            <button type="submit" class="btn btn-default">Search</button>
        </div>
    </form>
</div>
</%block>
