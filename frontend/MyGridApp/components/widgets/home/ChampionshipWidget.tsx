import { GlobalStyles, Constants, Colors } from "@/theme"
import { ViewProps, View, Dimensions, StyleSheet } from "react-native"
import { LiteButton, MainText, ShadowSetup, SpotLight } from "@/components/widgets"
import { scopedI18n } from "@/translations/i18n"

export type ChampionshipWidgetProps = ViewProps & {
  datas: any
}

export function ChampionshipWidget ({
  datas = null,
  ...otherProps
}: ChampionshipWidgetProps) {

  const t = scopedI18n('widgets.championshipWidget')
  const fontSize = Constants.fontSizes.header

  return (
    <View style={[GlobalStyles.button, GlobalStyles.mainWidget]}>
      <ShadowSetup/>
      <MainText bold={true} style={{ marginTop: Constants.spacing.buttonPadding, fontSize: fontSize }}>{t('championship')}</MainText>
      <View style={GlobalStyles.rowWidget}>
        <LiteButton style={style.button}>
          <SpotLight cx='45%' cy='45%' fx='20%' fy='20%' radius='60%' color={datas.wdc.leaderboard.ranks[0].team.color}/>
          <MainText style={{ marginBottom: 10 }}>{t('drivers')}</MainText>
          {datas.wdc.leaderboard.ranks.map((item: any) => (
            <View key={item.rank} style={{ flexDirection: 'row' }}>
              <MainText bold={true} style={{ marginEnd: 10 }}>{item.driver.codename}</MainText>
              <MainText >+ {item.score} Pts</MainText>
            </View>
          ))}
        </LiteButton>
        <LiteButton style={style.button}>
          <SpotLight cx='55%' cy='55%' fx='80%' fy='80%' radius='60%' color={datas.wcc.leaderboard.ranks[0].team.color}/>
          <MainText style={{ marginBottom: 10 }}>{t('constructors')}</MainText>
          <MainText bold={true} style={{ fontSize: Constants.fontSizes.header }}>{datas.wcc.leaderboard.ranks[0].team.name}</MainText>
          <MainText style={{ fontSize: Constants.fontSizes.header, marginBottom: 10 }}>+ {datas.wcc.leaderboard.ranks[0].score} Pts</MainText>
        </LiteButton>
      </View>
    </View>
  )

}

const dim = (Dimensions.get("window").width - Constants.spacing.mainWidgetMargin * 2 - Constants.spacing.buttonPadding * 3)/ 2 

const style = StyleSheet.create({
  button: {
    width: dim,
    height: dim,
    marginVertical: Constants.spacing.buttonPadding,
    padding: 0
  }
})