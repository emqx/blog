We're upgrading our global Serverless platform to enhance stability, performance, and observability. **Dedicated and BYOC deployments are not affected.**

## Upgrade Schedule

We'll perform upgrades across three regions to minimize business impact:

**Europe Region**

- **Date:** June 6, 2025
- **Time:** 02:00 - 03:00 UTC
- **Downtime:** 30-60 seconds

**Asia-Pacific Region**

- **Date:** June 10, 2025
- **Time:** 02:00 - 03:00 UTC
- **Downtime:** 30-60 seconds

**North America Region**

- **Date:** June 17, 2025
- **Time:** 02:00 - 03:00 UTC
- **Downtime:** 30-60 seconds

## What to Expect

### During Maintenance

- MQTT connections will drop briefly (2-3 times, 30-60 seconds each)
- Creating or modifying Serverless deployments will be disabled
- Workloads with no active devices are unaffected

### After Maintenance

- Service hostnames remain unchanged
- IP addresses will change
- Update firewall/security group allowlists if needed

## What You Need to Do

### Before Maintenance

- Ensure your MQTT clients support automatic reconnection
- Use domain names instead of IP addresses when possible

### After Maintenance

- Update IP allowlists if applicable
- Verify all devices reconnect successfully

## Regional Time Zones

### Europe Region (June 6)

- London: 03:00 - 04:00 (BST)
- Paris/Berlin: 04:00 - 05:00 (CEST)
- Dubai: 06:00 - 07:00

### Asia-Pacific Region (June 10)

- Singapore/Beijing: 10:00 - 11:00
- Tokyo: 11:00 - 12:00
- Sydney: 12:00 - 13:00

### North America Region (June 17)

- New York: 22:00 - 23:00 (June 16, EDT)
- Los Angeles: 19:00 - 20:00 (June 16, PDT)
- São Paulo: 23:00 - 00:00 (June 16-17, BRT)

## Support

- **Status updates:** https://status.emqxcloud.com
- **Technical support:** Submit a support ticket
- **Questions:** Our SRE team will prioritize your requests

We follow strict procedures to ensure smooth transitions. Thank you for your trust in EMQX Cloud.

**EMQX Cloud SRE Team**
