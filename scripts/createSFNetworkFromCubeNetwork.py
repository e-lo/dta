__copyright__   = "Copyright 2011 SFCTA"
__license__     = """
    This file is part of DTA.

    DTA is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    DTA is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with DTA.  If not, see <http://www.gnu.org/licenses/>.
"""
import datetime
import dta
import os
import sys

USAGE = r"""

 python createSFNetworkFromCubeNetwork.py geary_dynameq_net_dir geary_dynameq_net_prefix sf_cube_net_dir
 
 e.g.
 
 python createSFNetworkFromCubeNetwork.py Y:\dta\nwSubarea\2008 Base2008 Y:\dta\SanFrancisco\2010\CubeNetworkSource_renumberExternalsOnly
 
 """
 
if __name__ == '__main__':
    
    #if len(sys.argv) != 4:
    #    print USAGE
    #    sys.exit(2)
    
    #GEARY_DYNAMEQ_NET_DIR       = sys.argv[1] 
    #GEARY_DYNAMEQ_NET_PREFIX    = sys.argv[2]
    #SF_CUBE_NET_DIR             = sys.argv[3]

    #GEARY_DYNAMEQ_NET_DIR       = "/Users/michalis/Documents/workspace/dta/dev/testdata/dynameqNetwork_geary"
    #GEARY_DYNAMEQ_NET_PREFIX    = "Base"
    #SF_CUBE_NET_DIR = "/Users/michalis/Documents/workspace/dta/dev/testdata/CubeNetworkSource_renumberExternalsOnly/"    

    dta.setupLogging("dtaInfo.log", "dtaDebug.log", logToConsole=True)
    
    # The Geary network was created in an earlier Phase of work, so it already exists as
    # a Dynameq DTA network.  Initialize it from the Dynameq text files.
    #gearyScenario = dta.DynameqScenario(datetime.datetime(2010,1,1,0,0,0), 
    #                                    datetime.datetime(2010,1,1,4,0,0))


    #gearyScenario.read(dir=GEARY_DYNAMEQ_NET_DIR, file_prefix=GEARY_DYNAMEQ_NET_PREFIX) 
    #gearynetDta = dta.DynameqNetwork(scenario=gearyScenario)
    #gearynetDta.read(dir=GEARY_DYNAMEQ_NET_DIR, file_prefix=GEARY_DYNAMEQ_NET_PREFIX)
    
    # The rest of San Francisco currently exists as a Cube network.  Initialize it from
    # the Cube network files (which have been exported to dbfs.)
    sanfranciscoScenario = dta.DynameqScenario(datetime.datetime(2010,1,1,0,0,0), 
                                               datetime.datetime(2010,1,1,4,0,0))

    
    sanfranciscoCubeNet = dta.CubeNetwork(sanfranciscoScenario)
    sanfranciscoCubeNet.readNetfile \
      (netFile=os.path.join(SF_CUBE_NET_DIR,"SanFranciscoSubArea_2010.net"),
       nodeVariableNames=["N","X","Y"],
       linkVariableNames=["A","B","TOLL","USE",
                          "CAP","AT","FT","STREETNAME","TYPE",
                          "MTYPE","SPEED","DISTANCE","TIME",
                          "LANE_AM","LANE_OP","LANE_PM",
                          "BUSLANE_AM","BUSLANE_OP","BUSLANE_PM",
                          "TOLLAM_DA","TOLLAM_SR2","TOLLAM_SR3",
                          "TOLLPM_DA","TOLLPM_SR2","TOLLPM_SR3",
                          "TOLLEA_DA","TOLLEA_SR2","TOLLEA_SR3",
                          "TOLLMD_DA","TOLLMD_SR2","TOLLMD_SR3",
                          "TOLLEV_DA","TOLLEV_SR2","TOLLEV_SR3 ",
                          "VALUETOLL_FLAG","PASSTHRU",
                          "BUSTPS_AM","BUSTPS_OP","BUSTPS_PM",
                          ],
       centroidIds                      = range(1,999),
       nodeGeometryTypeEvalStr          = "Node.GEOMETRY_TYPE_INTERSECTION",
       nodeControlEvalStr               = "RoadNode.CONTROL_TYPE_SIGNALIZED",
       nodePriorityEvalStr              = "RoadNode.PRIORITY_TEMPLATE_NONE",
       nodeLabelEvalStr                 = "None",
       nodeLevelEvalStr                 = "None",
       linkReverseAttachedIdEvalStr     = "None", #TODO: fix?
       linkFacilityTypeEvalStr          = "int(FT)",
       linkLengthEvalStr                = "float(DISTANCE)",
       linkFreeflowSpeedEvalStr         = "float(SPEED)",
       linkEffectiveLengthFactorEvalStr = "1",
       linkResponseTimeFactorEvalStr    = "1.05",
       linkNumLanesEvalStr              = "2 if isConnector else (int(LANE_PM) + (1 if int(BUSLANE_PM)>0 else 0))",
       linkRoundAboutEvalStr            = "False",
       linkLevelEvalStr                 = "None",
       linkLabelEvalStr                 = '(STREETNAME if STREETNAME else "") + (" " if TYPE and STREETNAME else "") + (TYPE if TYPE else "")'
       )
    
    sanfrancsicoDynameqNet = dta.DynameqNetwork(scenario=sanfranciscoScenario)
    sanfrancsicoDynameqNet.deepcopy(sanfranciscoCubeNet)
    
    # add virtual nodes and links between Centroids and RoadNodes
    sanfrancsicoDynameqNet.insertVirtualNodeBetweenCentroidsAndRoadNodes(startVirtualNodeId=9000000, startVirtualLinkId=9000000)
    sanfrancsicoDynameqNet.removeCentroidConnectorsFromIntersections(splitReverseLinks=True)
    
    #sanfrancsicoDynameqNet.write(dir=r"Y:\dta\SanFrancisco\2010", file_prefix="sf")
    #sanfranciscoScenario.write(dir=r"Y:\dta\SanFrancisco\2010", file_prefix="sf")   
    exit(0)
    
    # Merge them together
    sanfranciscoNet = gearynetDta
    sanfranciscoNet.merge(sanfranciscoCubeNet)
    
    # Write the result.  sanfrancisco_dta is a DynameqNetwork
    sanfranciscoNet.write(dir = ".", file_prefix="SanFrancisco_")
    
