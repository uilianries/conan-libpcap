/**
 * \file
 * \brief List network card and collect information
 *
 * Copyright 2017 Uilian Ries <uilianries@gmail.com>
 */
#include <assert.h>
#include <stdlib.h>
#include <pcap.h>

int main(int argc, char **argv)
{
    char errbuf[PCAP_ERRBUF_SIZE] = {0};
    bpf_u_int32 netp = 0;
    bpf_u_int32 maskp = 0;

    // device lookup
    char* dev = pcap_lookupdev(errbuf);
    assert(dev != NULL);

    // use pcap to get net information
    int ret = pcap_lookupnet(dev,&netp,&maskp,errbuf);
    assert(ret == 0);

    return EXIT_SUCCESS;
}
