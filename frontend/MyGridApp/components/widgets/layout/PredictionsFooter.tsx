import { FrameProps, Frame, SpotLight, MainText, ShadowButton } from "@/components/widgets";
import { Constants } from "@/theme";
import { scopedI18n } from "@/translations/i18n";
import { View, StyleSheet } from "react-native";

export type PredictionsFooterProps = FrameProps & {
  potentialScore?: number,
  spotColor?: string | null,
  hasProno?: boolean,
  hasStarted?: boolean,
  changed?: boolean,
  handlePredictions?: () => Promise<unknown>;
}

export function PredictionsFooter ({
  potentialScore=0,
  spotColor=null,
  hasProno=false,
  hasStarted=false,
  changed=false,
  handlePredictions,
  ...otherProps
}: PredictionsFooterProps) {

  if ((!changed && !hasProno) || (!hasStarted && !changed)) {
    return
  }

  const t = scopedI18n('sessions.predictions')

  function footerContent () {
    if (hasStarted) {
      if (hasProno) {
        return (
          <View style={{ flexDirection: 'row', justifyContent: 'center', marginTop: Constants.spacing.listMargin }}>
            <MainText>{t('potentialScore')}</MainText>
            <MainText bold={true}>+ {potentialScore}{t('pts')}</MainText>
          </View>
        )
      }
      return null
    }

    if (changed) {
      return (
        <ShadowButton style={{ margin: 10 }} onPress={handlePredictions}>
          <MainText bold={true} style={{ fontSize: Constants.fontSizes.header }}>{t('makePrediction')}</MainText>
        </ShadowButton>
      )
    }
  }

  return (
    <Frame orientation="bottom" {...otherProps}>
      {spotColor && <View style={[StyleSheet.absoluteFill]}>
        <SpotLight color={spotColor} cx="60%" cy="60%" fx="90%" fy="90%" radius="70%" opacityStart="0.5"/>
      </View>}
      {footerContent()}
    </Frame>
  )
}