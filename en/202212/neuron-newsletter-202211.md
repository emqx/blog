We released Neuron 2.2.11 with optimizations and bug fixes in November. We are now working on v2.3, including adding an EtherNet/IP driver, improving the CNC FOOCAS driver, supporting remote OPC DA, and switching to NanoSDK to enhance the performance of data transmission.

## Add Ethernet/IP driver

EtherNet/IP is an industrial network protocol that adapts the Common Industrial Protocol (CIP) to standard Ethernet. It is managed by ODVA, a standards development organization and membership association whose members comprise the world’s leading industrial automation companies, and EtherNet/IP is its core technology.

EtherNet/IP driver in Neuron supports most data types, such as UINT8/INT8, UINT16/INT16, UINT32/INT32, UINT64/INT64, FLOAT, DOUBLE, STRING, BIT, and is capable of connecting to PLC devices that support the protocol Ethernet/IP.

## Improve CNC FOCAS driver

CNC FOOCAS driver now supports more data collection types, including CNC data and PMC data.

CNC data are mainly data related to Axis (positions, rates, etc.) as well as the data related to SPINDLES.

PMC data come from message demand, counter, data table, extended relay, single to CNC -> PMC, single to PMC -> CNC, keep relay, input single from other devices, output single from other devices, internal relay, changeable timer, signal to machine -> PMC, single to PMC -> machine. Each of them relates to multiple data types.

## Remote OPC DA

- Support DCOM on a Local Area Network (LAN).
- Provide GUI - Visualize the setting of DA/UA connections. You can visually observe data changes in nodes.
- Introduce new features to UA Server, such as enabling encrypted connections by default and offering username and password authentication.
- Change the name of the main program from opcshift to neuopc.
- Provide documentation for setting up a DCOM connection.
- Provide documentation for reading native data.

## Additional Updates

- Both WEB and API use port 7000.
- Improve the documentation for DTU.
- Improve the documentation of the official website for the upcoming 2.3 release.

## Bug fix

- Fix the issue that caused a reconnection exception when the MODBUS plugin is in server mode.





<section class="promotion">
    <div>
        Try Neuron for Free
    </div>
    <a href="https://www.emqx.com/en/try?product=neuron" class="button is-gradient px-5">Get Started →</a>
</section>
