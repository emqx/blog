随着企业数字化转型的不断深入，确保数据和信息安全变得日益重要。传统的访问控制方法往往需要为每个用户单独配置权限，这种方法管理复杂且漏洞百出，难以适应快速变化的业务需求。而基于角色的访问控制（RBAC）功能通过定义不同角色及其权限来简化权限管理，不仅能有效地控制用户对敏感信息和系统的访问，而且减轻了企业的运维负担。

NeuronEX 作为一款工业边缘网关软件，提供工业多协议接入与边缘计算能力。能够实现工业设备协议采集、工业各系统数据集成、边端数据过滤分析、AI算法集成以及数据转发和平台对接等功能，为工业场景提供低延迟的数据接入管理及智能分析服务。

本文将重点介绍 NeuronEX 中基于角色的访问控制功能。该功能支持用户创建不同的角色，不同的角色相对应不同的操作权限，以此达到权限隔离的目的，提高用户数据的安全性、合规性和灵活性。

## 用户管理

当前系统内置了一个用户名为 admin 的超级管理员用户，首次登录系统后可更改此用户的密码。为了实现基于角色访问控制功能，NeuronEX 新增了用户管理的功能，通过前端右上角的 **用户管理** 按钮即可进入。

![用户管理](https://assets.emqx.com/images/7f2ddcc2a0a81d5f69292bc46dda7aaf.png)

点击 **创建用户** 按钮，在弹出的页面中，需要填写新创建用户的名字、密码、角色和描述信息，在角色下拉选项框中，可选择 Administrator 和 Viewer 两种角色。填写好用户信息后，点击 **提交** 按钮即可保存。

![创建用户](https://assets.emqx.com/images/84bf72b36be872b6ead07c89b5644335.png)

此外用户创建好后，在用户列表中还支持重新编辑用户信息、修改密码和删除用户。

## 访问控制

NeuronEX 的权限与角色密切关联，并且不支持用户自定义权限与角色之间的对应关系，其对应关系由 NeuronEX 决定 。目前 Administrator 角色拥有 NeuronEX 所有的控制权限，可以查看、创建、修改和删除所有配置，而 Viewer 角色对一些配置只有查看的权限。

当创建好用户后，凭借新用户的登录信息即可登录系统。由于用户在创建时已被赋予了 Administrator 或者 Viewer 角色，因此在登录时该用户的权限已经确定。对于 Viewer 角色的用户来说，前端上的某些编辑按钮会呈现出不可编辑的状态。

![访问控制——Administrator](https://assets.emqx.com/images/c83012b399251ba1fa8926288f350893.png)

Administrator 角色可以创建新的南向设备

![访问控制——Viewer](https://assets.emqx.com/images/988dab1aa973d336d632005faf173b6b.png)

Viewer 角色无法创建新的南向设备

此外，访问控制除了在前端生效外，针对 NeuronEX API 的请求依旧生效，用户需要首先调用 /api/login 接口来获取 Token， 然后用获得的 Token 来调用对应的 NeuronEX API。以 Administrator 角色获得的 Token 可以请求任意 API，而用 Viewer 角色获得的 Token 请求没有权限的 API 时会返回 403 状态码。

## 总结

本文介绍了 NeuronEX 中基于角色的访问控制功能。通过支持创建多个用户并赋予用户 Administrator 或 Viewer 角色，并将角色与控制权限做了对应关系，实现了基本的访问控制功能。本例中，当用户分别以角色Administrator 和 Viewer 请求时，会根据角色限制用户的访问。该功能从 3.0.0 版本开始支持，欢迎体验。

<section class="promotion">
    <div>
        咨询 EMQ 技术专家
    </div>
    <a href="https://www.emqx.com/zh/contact?product=solutions" class="button is-gradient">联系我们 →</a>
</section>
