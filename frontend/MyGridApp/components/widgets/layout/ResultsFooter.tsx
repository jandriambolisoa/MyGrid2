import { FrameProps, Frame, MainText, SpotLight, Reaction } from "@/components/widgets"
import { GlobalStyles, Constants, Colors } from "@/theme"
import { View, StyleSheet, TouchableOpacity } from "react-native"
import { scopedI18n } from "@/translations/i18n"
import { performance } from "@/utils"
import { MaterialIcons } from "@expo/vector-icons"

export type ResultsFooterProps = FrameProps & {
  score?: number,
  potentialScore?: number,
  spotColor?: string | null,
  reactions?: any[],
  toggleReactions?: () => void;
}

export function ResultsFooter ({
  score=0,
  potentialScore=0,
  spotColor=null,
  reactions=[],
  toggleReactions,
  ...otherProps
}: ResultsFooterProps) {

  const t = scopedI18n('widgets.resultsFooter')

  return (
    <Frame orientation='bottom' {...otherProps}>
      {spotColor && <View style={[StyleSheet.absoluteFill]}>
        <SpotLight color={spotColor} cx="60%" cy="60%" fx="90%" fy="90%" radius="70%"/>
      </View>}
      <View style={StyleSheet.absoluteFill}>
        {reactions?.map((item: any, index: number) => 
          <Reaction
            item={item}
            key={index}
            startY={120}
            right='15%'
            duration={3000}
          />
        )}
        {toggleReactions && <TouchableOpacity
          style={{
            alignSelf: 'flex-end',
            width: Constants.spacing.backButtonSize,
            height: Constants.spacing.backButtonSize,
            alignItems: 'center',
            justifyContent: 'center'
          }}
          onPress={toggleReactions}
        >
          <MaterialIcons name='add-reaction' color={Colors.light.lightText} size={20}/>
        </TouchableOpacity>}
      </View>
      <View style={GlobalStyles.header}>
        <MainText style={{ fontSize: Constants.fontSizes.header, margin: 2 }} bold={true}>{t('totalScore')}+ {score} {t('pts')}</MainText>
        <MainText>{t('performance')}{performance(score, potentialScore)} %</MainText>
      </View>
    </Frame>
  )
}