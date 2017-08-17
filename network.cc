#include <string>
#include <fstream>
#include "ns3/core-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/internet-module.h"
#include "ns3/applications-module.h"
#include "ns3/network-module.h"
#include "ns3/packet-sink.h"
#include "ns3/wifi-module.h"
#include "ns3/mobility-module.h"
#include "ns3/csma-module.h"
#include "ns3/netanim-module.h"

//
//   Wifi 10.1.3.0
//                 AP
//  *    *    *    *
//  |    |    |    |    10.1.1.0
// n5   n6   n7   n0 -------------- n1   n2   n3   n4
//                   point-to-point  |    |    |    |
//                                   ================
//                                     LAN 10.1.2.0

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("Network");

int 
main (int argc, char *argv[])
{

  uint32_t nCsma = 3;
  uint32_t nWifi = 3;

  
  // p2p node creation and net device installation

  NodeContainer p2pNodes;
  p2pNodes.Create (2);

  PointToPointHelper pointToPoint;
  pointToPoint.SetDeviceAttribute ("DataRate", StringValue ("500Kbps"));
  pointToPoint.SetChannelAttribute ("Delay", StringValue ("5ms"));

  NetDeviceContainer p2pDevices;
  p2pDevices = pointToPoint.Install (p2pNodes);


  // csma node creation and net device installation

  NodeContainer csmaNodes;
  csmaNodes.Add (p2pNodes.Get (1));
  csmaNodes.Create (nCsma);

  CsmaHelper csma;
  csma.SetChannelAttribute ("DataRate", StringValue ("100Mbps"));
  csma.SetChannelAttribute ("Delay", TimeValue (NanoSeconds (6560)));

  NetDeviceContainer csmaDevices;
  csmaDevices = csma.Install (csmaNodes);

  
  // wifi node creation and net device installation

  NodeContainer wifiStaNodes;
  wifiStaNodes.Create (nWifi);
  NodeContainer wifiApNode = p2pNodes.Get (0);

  YansWifiChannelHelper channel = YansWifiChannelHelper::Default ();
  YansWifiPhyHelper phy = YansWifiPhyHelper::Default ();
  phy.SetChannel (channel.Create ());

  WifiHelper wifi;
  wifi.SetRemoteStationManager ("ns3::AarfWifiManager");

  WifiMacHelper mac;
  Ssid ssid = Ssid ("ns-3-ssid");
  mac.SetType ("ns3::StaWifiMac",
               "Ssid", SsidValue (ssid),
               "ActiveProbing", BooleanValue (false));

  NetDeviceContainer staDevices;
  staDevices = wifi.Install (phy, mac, wifiStaNodes);

  mac.SetType ("ns3::ApWifiMac",
               "Ssid", SsidValue (ssid));

  NetDeviceContainer apDevices;
  apDevices = wifi.Install (phy, mac, wifiApNode);


  // mobility model

  MobilityHelper mobility;

  mobility.SetPositionAllocator ("ns3::GridPositionAllocator",
                                 "MinX", DoubleValue (0.0),
                                 "MinY", DoubleValue (0.0),
                                 "DeltaX", DoubleValue (5.0),
                                 "DeltaY", DoubleValue (10.0),
                                 "GridWidth", UintegerValue (3),
                                 "LayoutType", StringValue ("RowFirst"));

  mobility.SetMobilityModel ("ns3::RandomWalk2dMobilityModel",
                             "Bounds", RectangleValue (Rectangle (-50, 50, -50, 50)));
  mobility.Install (wifiStaNodes);

  mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
  mobility.Install (wifiApNode);
  mobility.Install (csmaNodes);
  
  // error model
  
  Ptr<RateErrorModel> em = CreateObject<RateErrorModel> ();
  em->SetAttribute ("ErrorRate", DoubleValue (0.001));
  p2pDevices.Get (1)->SetAttribute ("ReceiveErrorModel", PointerValue (em));


  // internet stack

  InternetStackHelper stack;
  stack.Install (csmaNodes);
  stack.Install (wifiApNode);
  stack.Install (wifiStaNodes);


  // ipv4 addresses

  Ipv4AddressHelper address;

  address.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer p2pInterfaces;
  p2pInterfaces = address.Assign (p2pDevices);

  address.SetBase ("10.1.2.0", "255.255.255.0");
  Ipv4InterfaceContainer csmaInterfaces;
  csmaInterfaces = address.Assign (csmaDevices);

  address.SetBase ("10.1.3.0", "255.255.255.0");
  address.Assign (staDevices);
  address.Assign (apDevices);


  // applications

  uint16_t port = 9;
  uint32_t maxBytes = 10000; 

  BulkSendHelper source ("ns3::TcpSocketFactory",
                         InetSocketAddress (csmaInterfaces.GetAddress (nCsma), 
                                            port));
  source.SetAttribute ("MaxBytes", UintegerValue (maxBytes));
  
  ApplicationContainer sourceApps = source.Install (wifiStaNodes.Get (0));
  sourceApps.Start (Seconds (2.0));
  sourceApps.Stop (Seconds (10.0));
  
  BulkSendHelper source1 ("ns3::TcpSocketFactory",
                         InetSocketAddress (csmaInterfaces.GetAddress (nCsma-1), 
                                            port));  
  source1.SetAttribute ("MaxBytes", UintegerValue (maxBytes));
  
  ApplicationContainer sourceApps1 = source1.Install (wifiStaNodes.Get (1));
  sourceApps1.Start (Seconds (2.0));
  sourceApps1.Stop (Seconds (10.0));
   
  ApplicationContainer sourceApps2 = source1.Install (wifiStaNodes.Get (2));
  sourceApps2.Start (Seconds (2.0));
  sourceApps2.Stop (Seconds (10.0));

  PacketSinkHelper sink ("ns3::TcpSocketFactory",
                         InetSocketAddress (Ipv4Address::GetAny (), port));
                         
  ApplicationContainer sinkApps = sink.Install (csmaNodes.Get (nCsma));
  sinkApps.Start (Seconds (1.0));
  sinkApps.Stop (Seconds (10.0));
  
  ApplicationContainer sinkApps1 = sink.Install (csmaNodes.Get (nCsma-1));
  sinkApps1.Start (Seconds (1.0));
  sinkApps1.Stop (Seconds (10.0));


  // routing

  Ipv4GlobalRoutingHelper::PopulateRoutingTables ();


  // animation

  AnimationInterface anim ("netanim.xml");
  
  
  // tracing

  AsciiTraceHelper ascii;
  
  pointToPoint.EnableAsciiAll (ascii.CreateFileStream ("p2p.tr"));
  csma.EnableAsciiAll (ascii.CreateFileStream ("csma.tr"));
  phy.EnableAsciiAll (ascii.CreateFileStream ("wifi.tr"));


  // simulation

  Simulator::Stop (Seconds (10.0));
  Simulator::Run ();
  Simulator::Destroy ();
  
  
  // output
  
  Ptr<PacketSink> sink1 = DynamicCast<PacketSink> (sinkApps.Get (0));
  std::cout << "sink1:Total Bytes Received: " 
            << sink1->GetTotalRx () 
            << std::endl;
  Ptr<PacketSink> sink2 = DynamicCast<PacketSink> (sinkApps1.Get (0));
  std::cout << "sink2:Total Bytes Received: " 
            << sink2->GetTotalRx () 
            << std::endl;

  return 0;
}
