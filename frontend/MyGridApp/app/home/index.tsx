import { Container, MainText, ShadowButton } from "@/components/widgets"

export default function Home () {
  return (
    <Container>
      <ShadowButton style={{width: 200, height: 200}}>
        <MainText>Bienvenue sur Mygrid</MainText>
      </ShadowButton>
    </Container>
  )
}