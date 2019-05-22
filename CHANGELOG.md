<a name="cssi-api-0.1a1"></a>
## [cssi-api-0.1a1](https://github.com/brionmario/cssi-api/compare/682caa54ed2c92a89b5377fd664e9e6bfeb93037...cssi-api-0.1a1) (2019-05-22)

### Bug Fixes
- **app:** fix table recognition issue in migration :bug: ([42bda1a](https://github.com/brionmario/cssi-api/commit/42bda1ab496b940115e1a5868462496bb921db38))
- **models:** fix data type issues in models :bug: ([53b521c](https://github.com/brionmario/cssi-api/commit/53b521cef7201af70994b9d25e33256f4045dd85))
- **models:** fix minor validation issues in models ([56b39e6](https://github.com/brionmario/cssi-api/commit/56b39e69794eb9be68e0c9d092fca9a44fd745a4))

### Code Refactoring
- **app:** change folder structure :truck: ([77e49ae](https://github.com/brionmario/cssi-api/commit/77e49ae727da0c90da9029961d539eb7e8f2212c))
- **app:** move routes to v1 folder :truck: ([a2f368f](https://github.com/brionmario/cssi-api/commit/a2f368f1807ad4f4e5bc00edf88c5fe1985cb53c))
- **app:** remove flask restful code dependencies :recycle: ([1d97108](https://github.com/brionmario/cssi-api/commit/1d97108dedd7c16697271ee54076944e0ffbf349))
- **app:** rename applications to application :truck: ([33fcbdb](https://github.com/brionmario/cssi-api/commit/33fcbdbc7400605b9eef195f56ebc083bc0526c3))
- **config:** move app config to new folder :truck: ([46e6b17](https://github.com/brionmario/cssi-api/commit/46e6b17c3a88be2037942aa94bea4e5ee7980011))
- **core:** refactor entire codebase :recycle: ([5f772de](https://github.com/brionmario/cssi-api/commit/5f772de4db0e0c97c1ab66abde1b7bed54226078))
- **core:** remove base run script :fire: ([f0f0a8c](https://github.com/brionmario/cssi-api/commit/f0f0a8c42ce9dad58481a5aef94d31e323f5eca3))
- **events:** modify celery task init logic ([614658a](https://github.com/brionmario/cssi-api/commit/614658abdfdd5e8dc325f4bdd8a6b810b968e65e))
- **events:** move celery tasks to a separate file :truck: ([1a21a62](https://github.com/brionmario/cssi-api/commit/1a21a621c0d2bc855ddad9dd504cffe5112cce1b))
- **models:** put models in separate files :recycle: ([d1102c6](https://github.com/brionmario/cssi-api/commit/d1102c61260e5893ce96f80a67e9d36ad7f493b7))
- **models:** refactor application models and schemas ([a2f7a8e](https://github.com/brionmario/cssi-api/commit/a2f7a8ea831ce962193c9a312f093c8c2cdd7f2e))
- **routes:** refactor application routes ([bd0b739](https://github.com/brionmario/cssi-api/commit/bd0b73953bcf1054a4f3f9ed00616b7ac2dfec14))
- **routes:** remove initial validation in application GET ([e7d2a4d](https://github.com/brionmario/cssi-api/commit/e7d2a4d5d8a2509134a3b0f3142659066d4f1771))
- **routes:** remove unwanted imports ([964c509](https://github.com/brionmario/cssi-api/commit/964c509830f5b631dd5eb930c7c3ce3433813d59))

### Features
- **core:** add cors support :sparkles: ([f40a075](https://github.com/brionmario/cssi-api/commit/f40a07575bf64790f6ab0da56abe0282b2868064))
- **core:** add logging support :sparkles: ([e2d7641](https://github.com/brionmario/cssi-api/commit/e2d76418fa8d7b30837b254424ff77c18c35d44c))
- **core:** add plugin support :sparkles: ([e45efa9](https://github.com/brionmario/cssi-api/commit/e45efa9de906cd7c44c2da75e367d5cb0af44fb3))
- **core:** add websocket support :sparkles: ([fdfbfe0](https://github.com/brionmario/cssi-api/commit/fdfbfe05e315a5c3b109a269bc077d904594ce22))
- **core:** implement sessions related functionality :sparkes: ([97392b3](https://github.com/brionmario/cssi-api/commit/97392b3937410197a98cd0c33d8bca4468155ee8))
- **sessions:** add session status recording ability :sparkles: ([d23ff41](https://github.com/brionmario/cssi-api/commit/d23ff411cd1aec18bade6609cc8b3304813caa69))
- **views:** implement basic application routes :sparkles: ([9de44ea](https://github.com/brionmario/cssi-api/commit/9de44eae0b6fb5a34c9529dd1be483a9b2e97676))


