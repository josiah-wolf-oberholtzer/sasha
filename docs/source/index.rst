SASHA API Documentation
=======================
.. toctree::
   :maxdepth: 1

Core
----

bootstrap
~~~~~~~~~
.. toctree::
   :maxdepth: 1

   api/core/bootstrap/Bootstrap/Bootstrap
   api/core/bootstrap/Fixture/Fixture

config
~~~~~~
.. toctree::
   :maxdepth: 1

   api/core/config/SashaConfig/SashaConfig

domain
~~~~~~
.. toctree::
   :maxdepth: 1

   api/core/domain/Cluster/Cluster
   api/core/domain/DomainObject/DomainObject
   api/core/domain/Event/Event
   api/core/domain/Fingering/Fingering
   api/core/domain/Instrument/Instrument
   api/core/domain/InstrumentKey/InstrumentKey
   api/core/domain/InstrumentModel/InstrumentModel
   api/core/domain/Partial/Partial
   api/core/domain/Performer/Performer
   api/core/domain/RecordingLocation/RecordingLocation

plugins
~~~~~~~
.. toctree::
   :maxdepth: 1

   api/core/plugins/PluginGraph/PluginGraph

wrappers
~~~~~~~~
.. toctree::
   :maxdepth: 1

   api/core/wrappers/AudioDB/AudioDB
   api/core/wrappers/Convert/Convert
   api/core/wrappers/FFTExtract/FFTExtract
   api/core/wrappers/LAME/LAME
   api/core/wrappers/Playback/Playback
   api/core/wrappers/Wrapper/Wrapper

Asset Plugins
-------------

analysis
~~~~~~~~
.. toctree::
   :maxdepth: 1

   api/plugins/analysis/ChordAnalysis/ChordAnalysis
   api/plugins/analysis/ChromaAnalysis/ChromaAnalysis
   api/plugins/analysis/ConstantQAnalysis/ConstantQAnalysis
   api/plugins/analysis/LinearSpectrumAnalysis/LinearSpectrumAnalysis
   api/plugins/analysis/LogHarmonicityAnalysis/LogHarmonicityAnalysis
   api/plugins/analysis/LogPowerAnalysis/LogPowerAnalysis
   api/plugins/analysis/MFCCAnalysis/MFCCAnalysis
   api/plugins/analysis/PartialTrackingAnalysis/PartialTrackingAnalysis

audio
~~~~~
.. toctree::
   :maxdepth: 1

   api/plugins/audio/CroppedAudio/CroppedAudio
   api/plugins/audio/MP3Audio/MP3Audio
   api/plugins/audio/SourceAudio/SourceAudio

notation
~~~~~~~~
.. toctree::
   :maxdepth: 1

   api/plugins/notation/ChordNotation/ChordNotation
   api/plugins/notation/ChromaNotation/ChromaNotation
   api/plugins/notation/FingeringNotation/FingeringNotation

plotting
~~~~~~~~
.. toctree::
   :maxdepth: 1

   api/plugins/plotting/PartialTrackingPlot/PartialTrackingPlot

Tools
-----

analysistools
~~~~~~~~~~~~~
.. toctree::
   :maxdepth: 1

   api/tools/analysistools/Frame/Frame
   api/tools/analysistools/KMeansClustering/KMeansClustering
   api/tools/analysistools/PartialTracker/PartialTracker
   api/tools/analysistools/Peak/Peak
   api/tools/analysistools/PeakDetectionWorker/PeakDetectionWorker
   api/tools/analysistools/PeakDetector/PeakDetector
   api/tools/analysistools/Regression/Regression
   api/tools/analysistools/Track/Track
   api/tools/analysistools/report_tracks

collectiontools
~~~~~~~~~~~~~~~
.. toctree::
   :maxdepth: 1

   api/tools/collectiontools/Collection/Collection

diagramtools
~~~~~~~~~~~~
.. toctree::
   :maxdepth: 1

   api/tools/diagramtools/LilyPondSaxDiagram/LilyPondSaxDiagram

mediatools
~~~~~~~~~~
.. toctree::
   :maxdepth: 1

   api/tools/mediatools/play
