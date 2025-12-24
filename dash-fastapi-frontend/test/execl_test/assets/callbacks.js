window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        renderUniver: (id) => {
            // 参考示例：https://univer.ai/guides/sheet/getting-started/installation#using-cdn
            var {
                UniverCore,
                UniverDesign,
                UniverEngineRender,
                UniverEngineFormula,
                UniverSheetsFormulaUi,
                UniverDocs,
                UniverDocsUi,
                UniverUi,
                UniverSheets,
                UniverSheetsUi,
                UniverSheetsNumfmt,
                UniverSheetsFormula,
                UniverFacade,
            } = window

            var univer = new UniverCore.Univer({
                theme: UniverDesign.defaultTheme,
                locale: UniverCore.LocaleType.ZH_CN,
                locales: {
                    [UniverCore.LocaleType.ZH_CN]: UniverUMD['zh-CN'],
                },
            });

            univer.registerPlugin(UniverEngineRender.UniverRenderEnginePlugin);
            univer.registerPlugin(UniverEngineFormula.UniverFormulaEnginePlugin);

            univer.registerPlugin(UniverUi.UniverUIPlugin, {
                container: id,
            });

            univer.registerPlugin(UniverDocs.UniverDocsPlugin);
            univer.registerPlugin(UniverDocsUi.UniverDocsUIPlugin);

            univer.registerPlugin(UniverSheets.UniverSheetsPlugin);
            univer.registerPlugin(UniverSheetsUi.UniverSheetsUIPlugin);
            univer.registerPlugin(UniverSheetsNumfmt.UniverSheetsNumfmtPlugin);
            univer.registerPlugin(UniverSheetsFormula.UniverSheetsFormulaPlugin);
            univer.registerPlugin(UniverSheetsFormulaUi.UniverSheetsFormulaUIPlugin);

            univer.createUnit(UniverCore.UniverInstanceType.UNIVER_SHEET, {})

            const univerAPI = UniverFacade.FUniver.newAPI(univer)

            // 不在dash组件层面做实质性更新
            return window.dash_clientside.no_update
        }
    }
});