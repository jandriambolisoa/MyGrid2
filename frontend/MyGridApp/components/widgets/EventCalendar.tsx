import { Constants, GlobalStyles } from "@/theme"
import { TouchableOpacityProps, TouchableOpacity, Dimensions, FlatList, View, Animated } from "react-native"
import { MainText } from "@/components/widgets"
import { DateTime } from "luxon"
import { useRef } from "react"

export type EventCalendarWidgetProps = {
  size?: number,
  scroll?: Animated.Value,
  datas?: any,
  index?: number
} & TouchableOpacityProps

export function EventCalendarWidget ({
  size=0,
  scroll= new Animated.Value(0),
  datas=null,
  index=0,
  ...otherProps
}: EventCalendarWidgetProps) {

  const inputRange = [
    (index - 1) * (size + Constants.spacing.buttonPadding),
    index * (size + Constants.spacing.buttonPadding),
    (index + 1) * (size + Constants.spacing.buttonPadding),
  ];

  const scale = scroll.interpolate({ 
    inputRange,
    outputRange: [0.8, 1, 0.8],
    extrapolate: 'clamp'
  })

  return(
    <TouchableOpacity style={[GlobalStyles.button, { height: size, width: size, alignSelf: 'center', transform: [{ scale: scale }]  }]}>
      <MainText>{datas?.name}</MainText>
    </TouchableOpacity>
  )
}

export type EventCalendarProps = {
  datas?: any
}

export function EventCalendar ({
  datas = null,
  ...otherProps
}: EventCalendarProps) {
  
  const windowWidth = Dimensions.get('window').width;
  const size = windowWidth * 0.7;
  const blankSpace = (windowWidth - size) / 2;
  const firstPage = datas.findIndex((item: any) => DateTime.fromISO(item.datetime) > DateTime.now()) || datas.length - 1;
  const initialScrollX = firstPage * (size + Constants.spacing.buttonPadding);
  const scrollX = useRef(new Animated.Value(initialScrollX)).current;

  return (
    <FlatList
      data={datas}
      horizontal={true}
      snapToInterval={size + Constants.spacing.buttonPadding}
      decelerationRate="fast"
      showsHorizontalScrollIndicator={false}
      style={{ paddingBottom: Constants.spacing.mainWidgetMargin, alignSelf: 'stretch' }}
      contentContainerStyle={{ paddingHorizontal: blankSpace }}
      ItemSeparatorComponent={() => <View style={{ width: Constants.spacing.buttonPadding }}/>}
      contentOffset={{ x: initialScrollX, y: 0 }}
      onScroll={Animated.event(
        [{ nativeEvent: { contentOffset: { x: scrollX } } }],
        { useNativeDriver: false }
      )}
      renderItem={({ item, index }) => (
        <EventCalendarWidget size={size} scroll={scrollX} datas={item} index={index}/>
      )}
    />

  )
}