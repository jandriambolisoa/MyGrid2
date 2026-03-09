import { FrameProps, Frame, SpotLight, MainText, ShadowButton } from "@/components/widgets";
import { Constants, Colors } from "@/theme";
import { scopedI18n } from "@/translations/i18n";
import { View, StyleSheet, ActivityIndicator } from "react-native";

export type PredictionsFooterProps = FrameProps & {
  spotColor?: string | null,
  loading?: boolean
  handlePredictions?: () => Promise<unknown>;
}

export function PredictionsFooter ({
  spotColor=null,
  loading=false,
  handlePredictions,
  ...otherProps
}: PredictionsFooterProps) {

  const t = scopedI18n('sessions.predictions')

  function buttonContent () {
    if (loading) {
      return <ActivityIndicator color={Colors.light.lightText}/>
    }
    return <MainText bold={true} style={{ fontSize: Constants.fontSizes.header }}>{t('makePrediction')}</MainText>
  }

  return (
    <Frame orientation="bottom" {...otherProps}>
      {spotColor && <View style={[StyleSheet.absoluteFill]}>
        <SpotLight color={spotColor} cx="60%" cy="60%" fx="90%" fy="90%" radius="70%"/>
      </View>}
      <ShadowButton style={{ margin: 10 }} onPress={handlePredictions}>
        {buttonContent()}
      </ShadowButton>
    </Frame>
  )
}