import { StyleSheet, Text, type TextProps } from 'react-native';
import { Colors, Constants } from '@/theme';

type FontSize = 'small' | 'main' | 'header' | 'title' | 'big' | 'giant'; 

export type MainTextProps = TextProps & {
  type?: 'light' | 'dark';
  bold?: boolean;
  fontSize?: FontSize;
};

export function MainText({
  style,
  type = 'light',
  bold = false,
  fontSize = 'main',
  ...rest
}: MainTextProps) {

  const fontSizeMap: Record<FontSize, number> = {
    small: Constants.fontSizes.small,
    main: Constants.fontSizes.mainText,
    header: Constants.fontSizes.header,
    title: Constants.fontSizes.title,
    big: Constants.fontSizes.big,
    giant: Constants.fontSizes.giant,
  };

  return (
    <Text
      style={[
        {
          textAlign: 'center',
          fontSize: fontSizeMap[fontSize ?? 'main']
        },
        type === 'light' ? styles.light : undefined,
        type === 'dark' ? styles.dark : undefined,
        bold ? { fontFamily: 'AlteHaasGrotesk-Bold' } : { fontFamily: 'AlteHaasGrotesk' },
        style,
      ]}
      {...rest}
    />
  )
}

const styles = StyleSheet.create({
  light: {
    color: Colors.light.lightText,
  },
  dark: {
    color: Colors.light.darkText,
  }
})