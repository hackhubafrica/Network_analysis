#include <pcap.h>
#include <iostream>
#include <netinet/ip.h>
#include <netinet/tcp.h>

// Callback function called by pcap for every captured packet
void packet_handler(u_char *user_data, const struct pcap_pkthdr *pkthdr, const u_char *packet) {
    struct ip *ip_header = (struct ip *)(packet + 14);  // Skip Ethernet header
    struct tcphdr *tcp_header = (struct tcphdr *)(packet + 14 + ip_header->ip_hl * 4);

    std::cout << "Captured packet: "
              << "Source IP: " << inet_ntoa(ip_header->ip_src)
              << ", Destination IP: " << inet_ntoa(ip_header->ip_dst)
              << ", Source Port: " << ntohs(tcp_header->th_sport)
              << ", Destination Port: " << ntohs(tcp_header->th_dport) << std::endl;
}

int main() {
    char errbuf[PCAP_ERRBUF_SIZE];
    pcap_if_t *interfaces, *temp;
    pcap_t *handle;

    // Get a list of available network devices
    if (pcap_findalldevs(&interfaces, errbuf) == -1) {
        std::cerr << "Error finding devices: " << errbuf << std::endl;
        return 1;
    }

    // Open the first device
    handle = pcap_open_live(interfaces->name, BUFSIZ, 1, 1000, errbuf);
    if (handle == nullptr) {
        std::cerr << "Could not open device: " << errbuf << std::endl;
        return 2;
    }

    // Set a filter to capture only TCP packets on port 80
    struct bpf_program filter;
    std::string filter_exp = "tcp port 80";
    if (pcap_compile(handle, &filter, filter_exp.c_str(), 0, PCAP_NETMASK_UNKNOWN) == -1) {
        std::cerr << "Bad filter: " << pcap_geterr(handle) << std::endl;
        return 2;
    }

    if (pcap_setfilter(handle, &filter) == -1) {
        std::cerr << "Error setting filter: " << pcap_geterr(handle) << std::endl;
        return 2;
    }

    // Start capturing packets
    pcap_loop(handle, 10, packet_handler, nullptr);

    // Clean up
    pcap_freealldevs(interfaces);
    pcap_close(handle);

    return 0;
}
