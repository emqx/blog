We are proud to announce the first public release of a new open-source [functional programming language - Hamler](https://www.hamler-lang.org/). **Hamler** is a strongly-typed language with compile-time type checking and built-in support for concurrency and distribution. It empowers industries to build the next generation of scalable, reliable, realtime applications, especially for 5G, IoT and edge computing.

## Why Hamler?

For almost a decade, we have been developing software systems based on Erlang/OTP, especially our main product [EMQ X](https://github.com/emqx/emqx) - the scalable open-source MQTT broker. So, we have always believed that Erlang is a masterpiece of engineering. With amazing concurrency, distribution and fault tolerance, it is one of the few general-purpose language platforms able to properly handle concurrency and soft realtime.

However, from years of experience developing Erlang programs, we have been looking to solve two problems: the compile-time type system and the more friendly language syntax. A powerful compile-time type system helps build more reliable software systems; while a more friendly syntax helps to build a prosperous developer community.

It has taken nearly 20 years for academia and industry to find a solution. Started with Prof. [Philip Wadler](https://en.wikipedia.org/wiki/Philip_Wadler) and [Simon Marlow](https://simonmar.github.io/) in 2000, type annotation and **Dialyzer** a static analysis tool were introduced for Erlang.

- Simon Marlow & Philip Wadler (1997): [A practical subtyping system for Erlang](https://homepages.inf.ed.ac.uk/wadler/papers/erlang/erlang.pdf)
- Philip Wadler (2002):  [The great type hope](https://homepages.inf.ed.ac.uk/wadler/papers/erlang/erlang-slides.pdf)

Since 2008, there have been about 20 projects in the industry trying to solve the problem. [Elixir][ElixirSite] language project introduced Ruby syntax and attracted developers from the Ruby On Rails community! The [Akka][AkkaSite] project imitated the implementation of Erlang/OTP, but lost the soft real-time feature of Erlang/OTP. [Well-Typed][WellTypedSite]'s the [Cloud Haskell][CloudHaskellSite] project attempts to simulate the implementation of Erlang/ OTP in Haskell, the project is currently stalled. There are others like [lfe][lfeSite] introduced Lisp syntax, [alpaca][alpacaSite]、[efene][efeneSite]、[elchemy][elchemySite]、[gleam][gleamSite] etc. have attempted to introduce ML style syntax and static types, most of which are still in their early stage of development.

The [**EMQ**](https://github.com/emqx/) team has made another attempt to address these issues with a new design approach. And today, we present the industry the release of Hamler Language 0.1!

[AkkaSite]: https://akka.io/ "Akka Site"
[alpacaSite]: https://github.com/alpaca-lang/alpaca/ "alpaca Site"
[CloudHaskellSite]: https://github.com/haskell-distributed/ "CloudHaskell Site"
[ElixirSite]: https://github.com/elixir-lang/elixir/ "Elixir Site"
[efeneSite]: https://github.com/efene/efene/ "efene Site"
[elchemySite]: https://github.com/wende/elchemy/ "elchemy Site"
[gleamSite]: https://github.com/gleam-lang/gleam/ "gleam Site"
[lfeSite]: https://github.com/rvirding/lfe/ "lfe Site"
[WellTypedSite]: https://www.well-typed.com/ "Well-Typed Site"

## **Hamler Core Features**

The core features of Hamler, a functional programming language running on Erlang VM with the Haskell-like syntax, can be summarized as follows:

- Haskell and ML-like friendly syntax
- Type checking and inference at compile time
- Concurrency, soft real-time support at runtime

Combined with our years of experience and understanding in developing Erlang and Haskell programs, the Hamler language supports most of the major features of functional programming that we believe will help the industry better prepare for the coming wave of development in 5G, IoT and edge computing, and attract more developers to use the Erlang VM - BEAM.

- Functional programming
- Haskell and ML style
- ADT and Type Checking/Inference
- Functions, higher-order functions
- Currying and partial application
- Pattern matching, and Guards
- List comprehension
- Applicative and Monad
- Advanced module system
- Built-in concurrency

## **The Hamler Compiler**

The Hamler source code is parsed to generate CST, then CoreErlang's IR is generated after CST -> AST -> CoreFn's syntax tree transformation, syntax analysis and type checking. The code is then used by the Erlang compiler to generate the final Beam bytecode.

The Hamler compiler architecture is shown below:

![hamler-compiler](https://static.emqx.net/images/28c4497efb066b3162c6b921bd3cd320.png)

The Hamler 0.1 compiler was initially attempted to be implemented based on the GHC 8.10.1, but was later changed to adapt from [Purescript](https://www.purescript.org/) Compiler 0.13.6's implementation.

## **Documentation**

- [Cheatsheet](https://github.com/hamler-lang/documentation/blob/master/Cheatsheet.md)
- [Documentation](https://github.com/hamler-lang/documentation/)

## **Community, discussion and supports**

You can reach the **Hamler** community and core team via the following channels:

- [Slack - emqx/hamler-lang](https://slack-invite.emqx.io/)
- [Twitter - @hamlerlang](https://twitter.com/hamlerlang/)
- [Reddit - /r/HamlerLang](https://www.reddit.com/r/HamlerLang/)
- [Medium - @hamlerlang](https://medium.com/@hamlerlang/)

## **Contributing**

To contribute to **Hamler** project:

- Report issues: submit any bugs, issues to [hamler/issues][hamler-issues]
- Contribute code: Fork the project, and submit feature requests to [hamler-lang/hamler][hamler-project].
- Submit a proposal: Fork the [hamler-wiki][hamler-wiki] project and submit pull request

## **Core Team**

The Hamler core team comes from [EMQ Technologies Co., Ltd.](https://www.emqx.com/en) now.

- [Feng Lee](https://github.com/emqplus): The designer of Hamler language.
- [Yang M](https://github.com/EMQ-YangM): Implemented Hamler Compiler
- [S Hu](https://github.com/SjWho): Maintainer of the documentations
- [Shawn](https://github.com/terry-xiaoyu): Contributed [rebar3_hamler][rebar3_hamler] plugin
- [Rory Z](https://github.com/zhanghongtong): Contributed [homebrew][homebrew] install package
- [wivwiv](https://github.com/wivwiv): Designer of hamler-lang.org website
- [CrazyWisdom](https://github.com/CrazyWisdom): Maintainer of hamler-lang.org
- [ysfscream](https://github.com/ysfscream): Maintainer of hamler-lang.org
- [juan6666](https://github.com/juan6666)：Designer of Hamler language logo

## **About EMQ**

[**EMQ**](https://www.emqx.com/en) is an open source software company providing highly-scalable, real-time messaging and streaming platform for IoT applications in 5G Era.

[hamler-issues]: https://github.com/hamler-lang/hamler/issues
[hamler-project]: https://github.com/hamler-lang/hamler
[hamler-wiki]: https://github.com/hamler-lang/hamler-wiki
[homebrew]: https://github.com/hamler-lang/homebrew-hamler
[rebar3_hamler]: https://github.com/hamler-lang/rebar3_hamler