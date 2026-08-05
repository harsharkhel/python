import svgPaths from "./svg-knhuv3k2vz";
import imgCastleLogo from "./2c6d36ef214f02bc3fe4558e2ef8ef64adf65d4e.png";
import imgChessBoardWithGoldKingAndSilverPiecesRepresentingStrategy from "./c654f55e054bdd0de6110c2a915c960b3fa0c1ff.png";

function CastleLogo() {
  return (
    <div className="max-w-[295.5px] relative shrink-0 size-[48px]" data-name="Castle Logo">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <img alt="" className="absolute left-0 max-w-none size-full top-0" src={imgCastleLogo} />
      </div>
    </div>
  );
}

function Heading() {
  return (
    <div className="content-stretch flex flex-col items-start pt-[16px] relative shrink-0 w-full" data-name="Heading 1">
      <div className="[word-break:break-word] flex flex-col font-['Inter:Bold',sans-serif] font-bold justify-center leading-[0] not-italic relative shrink-0 text-[30px] text-white tracking-[-0.75px] w-full">
        <p className="leading-[36px]">Sign In</p>
      </div>
    </div>
  );
}

function Container1() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Container">
      <div className="[word-break:break-word] flex flex-col font-['Inter:Regular',sans-serif] font-normal justify-center leading-[0] not-italic relative shrink-0 text-[#9ca3af] text-[16px] w-full">
        <p className="leading-[24px] mb-0">Welcome back to the strategic</p>
        <p className="leading-[24px]">platform.</p>
      </div>
    </div>
  );
}

function Container() {
  return (
    <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-name="Container">
      <CastleLogo />
      <Heading />
      <Container1 />
    </div>
  );
}

function Margin() {
  return (
    <div className="content-stretch flex flex-col items-start pb-[32px] relative shrink-0 w-full" data-name="Margin">
      <Container />
    </div>
  );
}

function Label() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Label">
      <div className="[word-break:break-word] flex flex-col font-['Inter:Medium',sans-serif] font-medium justify-center leading-[0] not-italic relative shrink-0 text-[#9ca3af] text-[14px] w-full">
        <p className="leading-[20px]">Email Address</p>
      </div>
    </div>
  );
}

function Container3() {
  return (
    <div className="flex-[1_0_0] min-w-px relative" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col items-start overflow-clip relative rounded-[inherit] size-full">
        <div className="[word-break:break-word] flex flex-col font-['Inter:Regular',sans-serif] font-normal justify-center leading-[0] not-italic relative shrink-0 text-[#6b7280] text-[16px] w-full">
          <p className="leading-[normal]">you@company.com</p>
        </div>
      </div>
    </div>
  );
}

function Input() {
  return (
    <div className="bg-[#242424] relative rounded-[8px] shrink-0 w-full" data-name="Input">
      <div className="flex flex-row justify-center overflow-clip rounded-[inherit] size-full">
        <div className="content-stretch flex items-start justify-center px-[13px] py-[11px] relative size-full">
          <Container3 />
        </div>
      </div>
      <div aria-hidden className="absolute border border-[#404040] border-solid inset-0 pointer-events-none rounded-[8px]" />
    </div>
  );
}

function Container2() {
  return (
    <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-name="Container">
      <Label />
      <Input />
    </div>
  );
}

function Label1() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Label">
      <div className="[word-break:break-word] flex flex-col font-['Inter:Medium',sans-serif] font-medium justify-center leading-[0] not-italic relative shrink-0 text-[#9ca3af] text-[14px] w-full">
        <p className="leading-[20px]">Password</p>
      </div>
    </div>
  );
}

function Container5() {
  return (
    <div className="flex-[1_0_0] min-w-px relative" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col items-start overflow-clip relative rounded-[inherit] size-full">
        <div className="[word-break:break-word] flex flex-col font-['Inter:Regular',sans-serif] font-normal justify-center leading-[0] not-italic relative shrink-0 text-[#6b7280] text-[16px] w-full">
          <p className="leading-[normal]">••••••••</p>
        </div>
      </div>
    </div>
  );
}

function Input1() {
  return (
    <div className="bg-[#242424] relative rounded-[8px] shrink-0 w-full" data-name="Input">
      <div className="flex flex-row justify-center overflow-clip rounded-[inherit] size-full">
        <div className="content-stretch flex items-start justify-center px-[13px] py-[11px] relative size-full">
          <Container5 />
        </div>
      </div>
      <div aria-hidden className="absolute border border-[#404040] border-solid inset-0 pointer-events-none rounded-[8px]" />
    </div>
  );
}

function Container4() {
  return (
    <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-name="Container">
      <Label1 />
      <Input1 />
    </div>
  );
}

function Label2() {
  return (
    <div className="content-stretch flex gap-[8px] items-center relative shrink-0" data-name="Label">
      <div className="bg-[#242424] relative rounded-[4px] shrink-0 size-[16px]" data-name="Input">
        <div aria-hidden className="absolute border border-[#404040] border-solid inset-0 pointer-events-none rounded-[4px]" />
      </div>
      <div className="[word-break:break-word] flex flex-col font-['Inter:Regular',sans-serif] font-normal justify-center leading-[0] not-italic relative shrink-0 text-[#9ca3af] text-[14px] whitespace-nowrap">
        <p className="leading-[20px]">Remember me</p>
      </div>
    </div>
  );
}

function Link() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0" data-name="Link">
      <div className="[word-break:break-word] flex flex-col font-['Inter:Regular',sans-serif] font-normal justify-center leading-[0] not-italic relative shrink-0 text-[#cda434] text-[14px] whitespace-nowrap">
        <p className="leading-[20px]">Forgot password?</p>
      </div>
    </div>
  );
}

function Container6() {
  return (
    <div className="content-stretch flex items-center justify-between relative shrink-0 w-full" data-name="Container">
      <Label2 />
      <Link />
    </div>
  );
}

function Button() {
  return (
    <div className="bg-[#cda434] content-stretch flex items-center justify-center py-[12px] relative rounded-[8px] shrink-0 w-full" data-name="Button">
      <div className="[word-break:break-word] flex flex-col font-['Inter:Bold',sans-serif] font-bold justify-center leading-[0] not-italic relative shrink-0 text-[16px] text-black text-center tracking-[0.8px] uppercase whitespace-nowrap">
        <p className="leading-[24px]">SIGN IN</p>
      </div>
    </div>
  );
}

function Form() {
  return (
    <div className="content-stretch flex flex-col gap-[23.5px] items-start relative shrink-0 w-full" data-name="Form">
      <Container2 />
      <Container4 />
      <Container6 />
      <Button />
    </div>
  );
}

function Container7() {
  return (
    <div className="relative shrink-0 w-full" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col items-center relative size-full">
        <div className="[word-break:break-word] flex flex-col font-['Inter:Regular',sans-serif] font-normal justify-center leading-[0] not-italic relative shrink-0 text-[#6b7280] text-[14px] text-center whitespace-nowrap">
          <p className="leading-[20px]">Or continue with</p>
        </div>
      </div>
    </div>
  );
}

function Container9() {
  return (
    <div className="relative shrink-0" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col items-center relative size-full">
        <div className="[word-break:break-word] flex flex-col font-['Inter:Regular',sans-serif] font-normal justify-center leading-[0] not-italic relative shrink-0 text-[14px] text-center text-white whitespace-nowrap">
          <p className="leading-[20px]">Google</p>
        </div>
      </div>
    </div>
  );
}

function Button1() {
  return (
    <div className="content-stretch flex items-center justify-center pl-[46.19px] pr-[46.18px] py-[9px] relative rounded-[8px] shrink-0" data-name="Button">
      <div aria-hidden className="absolute border border-[#1f2937] border-solid inset-0 pointer-events-none rounded-[8px]" />
      <Container9 />
    </div>
  );
}

function Container10() {
  return (
    <div className="relative shrink-0" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col items-center relative size-full">
        <div className="[word-break:break-word] flex flex-col font-['Inter:Regular',sans-serif] font-normal justify-center leading-[0] not-italic relative shrink-0 text-[14px] text-center text-white whitespace-nowrap">
          <p className="leading-[20px]">LinkedIn</p>
        </div>
      </div>
    </div>
  );
}

function Button2() {
  return (
    <div className="content-stretch flex items-center justify-center pl-[42.02px] pr-[42.01px] py-[9px] relative rounded-[8px] shrink-0" data-name="Button">
      <div aria-hidden className="absolute border border-[#1f2937] border-solid inset-0 pointer-events-none rounded-[8px]" />
      <Container10 />
    </div>
  );
}

function Container8() {
  return (
    <div className="relative shrink-0 w-full" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex gap-[16px] items-start relative size-full">
        <Button1 />
        <Button2 />
      </div>
    </div>
  );
}

function HorizontalBorder() {
  return (
    <div className="content-stretch flex flex-col gap-[16px] items-start pt-[33px] relative shrink-0 w-full" data-name="HorizontalBorder">
      <div aria-hidden className="absolute border-[#1f2937] border-solid border-t inset-0 pointer-events-none" />
      <Container7 />
      <Container8 />
    </div>
  );
}

function Margin1() {
  return (
    <div className="content-stretch flex flex-col items-start pt-[32px] relative shrink-0 w-full" data-name="Margin">
      <HorizontalBorder />
    </div>
  );
}

function Background() {
  return (
    <div className="absolute bg-[#1a1a1a] content-stretch flex flex-col inset-[1px_35.14%_1px_30.88%] items-start justify-center p-[48px]" data-name="Background">
      <Margin />
      <Form />
      <Margin1 />
    </div>
  );
}

function ChessBoardWithGoldKingAndSilverPiecesRepresentingStrategy() {
  return (
    <div className="absolute inset-0 opacity-80" data-name="Chess board with gold king and silver pieces representing strategy">
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <img alt="" className="absolute h-full left-[-100.03%] max-w-none top-0 w-[300.07%]" src={imgChessBoardWithGoldKingAndSilverPiecesRepresentingStrategy} />
      </div>
    </div>
  );
}

function Heading1() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Heading 2">
      <div className="[word-break:break-word] flex flex-col font-['Inter:Bold',sans-serif] font-bold justify-center leading-[0] not-italic relative shrink-0 text-[24px] text-white tracking-[-0.6px] whitespace-nowrap">
        <p className="leading-[32px]">Master Your Strategy</p>
      </div>
    </div>
  );
}

function Container11() {
  return (
    <div className="content-stretch flex flex-col items-start pb-[0.625px] relative shrink-0 w-full" data-name="Container">
      <div className="[word-break:break-word] flex flex-col font-['Inter:Light',sans-serif] font-light justify-center leading-[0] not-italic relative shrink-0 text-[#9ca3af] text-[14px] whitespace-nowrap">
        <p className="leading-[22.75px] mb-0">Precision and foresight in every business move.</p>
        <p className="leading-[22.75px]">Log in to access your command center.</p>
      </div>
    </div>
  );
}

function OptionalSmallBrandQuoteOverlay() {
  return (
    <div className="absolute bottom-[32px] content-stretch flex flex-col gap-[6.875px] items-start left-[32px] max-w-[384px]" data-name="Optional: Small brand/quote overlay">
      <Heading1 />
      <Container11 />
    </div>
  );
}

function LeftSideHeroImageTakingUpHalfTheScreenOnDesktop() {
  return (
    <div className="absolute bg-black inset-[1px_69.12%_1px_0.09%]" data-name="Left side: Hero Image taking up half the screen on desktop">
      <ChessBoardWithGoldKingAndSilverPiecesRepresentingStrategy />
      <div className="absolute bg-gradient-to-r from-[rgba(0,0,0,0.6)] inset-0 to-[rgba(0,0,0,0)]" data-name="Subtle gradient overlay for text readability if text was placed here" />
      <OptionalSmallBrandQuoteOverlay />
    </div>
  );
}

function Heading2() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Heading 1">
      <div className="[word-break:break-word] flex flex-col font-['Inter:Bold',sans-serif] font-bold justify-center leading-[0] not-italic relative shrink-0 text-[30px] text-white tracking-[-0.75px] w-full">
        <p className="leading-[36px]">Sign In</p>
      </div>
    </div>
  );
}

function Container12() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Container">
      <div className="[word-break:break-word] flex flex-col font-['Inter:Regular',sans-serif] font-normal justify-center leading-[0] not-italic relative shrink-0 text-[#9ca3af] text-[14px] w-full">
        <p className="leading-[20px]">Welcome back to the strategic platform.</p>
      </div>
    </div>
  );
}

function HeaderSectionOfTheForm() {
  return (
    <div className="content-stretch flex flex-col gap-[8px] items-start relative shrink-0 w-full" data-name="Header section of the form">
      <Heading2 />
      <Container12 />
    </div>
  );
}

function HeaderSectionOfTheFormMargin() {
  return (
    <div className="content-stretch flex flex-col items-start pb-[40px] relative shrink-0 w-full" data-name="Header section of the form:margin">
      <HeaderSectionOfTheForm />
    </div>
  );
}

function Label3() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Label">
      <div className="[word-break:break-word] flex flex-col font-['Inter:Medium',sans-serif] font-medium justify-center leading-[0] not-italic relative shrink-0 text-[#d1d5db] text-[14px] w-full">
        <p className="leading-[20px]">Email Address</p>
      </div>
    </div>
  );
}

function Container13() {
  return (
    <div className="flex-[1_0_0] min-w-px relative" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col items-start overflow-clip relative rounded-[inherit] size-full">
        <div className="[word-break:break-word] flex flex-col font-['Inter:Regular',sans-serif] font-normal justify-center leading-[0] not-italic relative shrink-0 text-[#6b7280] text-[16px] w-full">
          <p className="leading-[normal]">you@company.com</p>
        </div>
      </div>
    </div>
  );
}

function Input2() {
  return (
    <div className="bg-[#242424] relative rounded-[6px] shrink-0 w-full" data-name="Input">
      <div className="flex flex-row justify-center overflow-clip rounded-[inherit] size-full">
        <div className="content-stretch flex items-start justify-center px-[17px] py-[15px] relative size-full">
          <Container13 />
        </div>
      </div>
      <div aria-hidden className="absolute border border-[#404040] border-solid inset-0 pointer-events-none rounded-[6px] shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)]" />
    </div>
  );
}

function EmailInputGroup() {
  return (
    <div className="content-stretch flex flex-col gap-[6px] items-start relative shrink-0 w-full" data-name="Email Input Group">
      <Label3 />
      <Input2 />
    </div>
  );
}

function Label4() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Label">
      <div className="[word-break:break-word] flex flex-col font-['Inter:Medium',sans-serif] font-medium justify-center leading-[0] not-italic relative shrink-0 text-[#d1d5db] text-[14px] w-full">
        <p className="leading-[20px]">Password</p>
      </div>
    </div>
  );
}

function Container14() {
  return (
    <div className="flex-[1_0_0] min-w-px relative" data-name="Container">
      <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col items-start overflow-clip relative rounded-[inherit] size-full">
        <div className="[word-break:break-word] flex flex-col font-['Inter:Regular',sans-serif] font-normal justify-center leading-[0] not-italic relative shrink-0 text-[#6b7280] text-[16px] w-full">
          <p className="leading-[normal]">••••••••</p>
        </div>
      </div>
    </div>
  );
}

function Input3() {
  return (
    <div className="bg-[#242424] relative rounded-[6px] shrink-0 w-full" data-name="Input">
      <div className="flex flex-row justify-center overflow-clip rounded-[inherit] size-full">
        <div className="content-stretch flex items-start justify-center px-[17px] py-[15px] relative size-full">
          <Container14 />
        </div>
      </div>
      <div aria-hidden className="absolute border border-[#404040] border-solid inset-0 pointer-events-none rounded-[6px] shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)]" />
    </div>
  );
}

function PasswordInputGroup() {
  return (
    <div className="content-stretch flex flex-col gap-[6px] items-start relative shrink-0 w-full" data-name="Password Input Group">
      <Label4 />
      <Input3 />
    </div>
  );
}

function LabelMargin() {
  return (
    <div className="content-stretch flex flex-col items-start pl-[8px] relative shrink-0" data-name="Label:margin">
      <div className="[word-break:break-word] flex flex-col font-['Inter:Regular',sans-serif] font-normal justify-center leading-[0] not-italic relative shrink-0 text-[#9ca3af] text-[14px] whitespace-nowrap">
        <p className="leading-[20px]">Remember me</p>
      </div>
    </div>
  );
}

function Container15() {
  return (
    <div className="content-stretch flex items-center relative shrink-0" data-name="Container">
      <div className="bg-[#242424] relative rounded-[4px] shrink-0 size-[16px]" data-name="Input">
        <div aria-hidden className="absolute border border-[#4b5563] border-solid inset-0 pointer-events-none rounded-[4px]" />
      </div>
      <LabelMargin />
    </div>
  );
}

function Container16() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0" data-name="Container">
      <div className="[word-break:break-word] flex flex-col font-['Inter:Medium',sans-serif] font-medium justify-center leading-[0] not-italic relative shrink-0 text-[#cda434] text-[14px] whitespace-nowrap">
        <p className="leading-[20px]">Forgot password?</p>
      </div>
    </div>
  );
}

function RememberMeForgotPasswordRow() {
  return (
    <div className="content-stretch flex items-center justify-between relative shrink-0 w-full" data-name="Remember Me & Forgot Password Row">
      <Container15 />
      <Container16 />
    </div>
  );
}

function SubmitButton() {
  return (
    <div className="bg-[#cda434] drop-shadow-[0px_1px_1px_rgba(0,0,0,0.05)] relative rounded-[6px] shrink-0 w-full" data-name="Submit Button">
      <div aria-hidden className="absolute border border-[rgba(0,0,0,0)] border-solid inset-0 pointer-events-none rounded-[6px]" />
      <div className="flex flex-row justify-center size-full">
        <div className="content-stretch flex items-start justify-center px-[17px] py-[13px] relative size-full">
          <div className="[word-break:break-word] flex flex-col font-['Inter:Semi_Bold',sans-serif] font-semibold justify-center leading-[0] not-italic relative shrink-0 text-[14px] text-black text-center tracking-[0.7px] uppercase whitespace-nowrap">
            <p className="leading-[20px]">SIGN IN</p>
          </div>
        </div>
      </div>
    </div>
  );
}

function TheForm() {
  return (
    <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-name="The Form">
      <EmailInputGroup />
      <PasswordInputGroup />
      <RememberMeForgotPasswordRow />
      <SubmitButton />
    </div>
  );
}

function Container17() {
  return (
    <div className="absolute content-stretch flex inset-0 items-center justify-center" data-name="Container">
      <div className="flex-[1_0_0] h-px min-w-px relative" data-name="Horizontal Divider">
        <div aria-hidden className="absolute border-[#374151] border-solid border-t inset-0 pointer-events-none" />
      </div>
    </div>
  );
}

function Background1() {
  return (
    <div className="bg-[#121212] content-stretch flex flex-col items-start px-[8px] relative self-stretch shrink-0" data-name="Background">
      <div className="[word-break:break-word] flex flex-col font-['Inter:Regular',sans-serif] font-normal justify-center leading-[0] not-italic relative shrink-0 text-[#6b7280] text-[14px] whitespace-nowrap">
        <p className="leading-[20px]">Or continue with</p>
      </div>
    </div>
  );
}

function Container18() {
  return (
    <div className="content-stretch flex items-start justify-center relative shrink-0 w-full" data-name="Container">
      <Background1 />
    </div>
  );
}

function Divider() {
  return (
    <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Divider">
      <Container17 />
      <Container18 />
    </div>
  );
}

function DividerMargin() {
  return (
    <div className="content-stretch flex flex-col items-start pt-[32px] relative shrink-0 w-full" data-name="Divider:margin">
      <Divider />
    </div>
  );
}

function Svg() {
  return (
    <div className="relative shrink-0 size-[20px]" data-name="SVG">
      <svg className="absolute block inset-0 size-full" fill="none" height="20" preserveAspectRatio="none" viewBox="0 0 20 20" width="20">
        <g id="SVG">
          <path d={svgPaths.p29ad9380} fill="#4285F4" id="Vector" />
          <path d={svgPaths.p73c0a80} fill="#34A853" id="Vector_2" />
          <path d={svgPaths.p1f69ba00} fill="#FBBC05" id="Vector_3" />
          <path d={svgPaths.p3d0b3f00} fill="#EA4335" id="Vector_4" />
        </g>
      </svg>
    </div>
  );
}

function LinkGoogle() {
  return (
    <div className="bg-[#242424] content-stretch drop-shadow-[0px_1px_1px_rgba(0,0,0,0.05)] flex gap-[8px] items-center justify-center px-[17px] py-[11px] relative rounded-[6px] shrink-0 w-[129.88px]" data-name="Link - Google">
      <div aria-hidden className="absolute border border-[#374151] border-solid inset-0 pointer-events-none rounded-[6px]" />
      <Svg />
      <div className="[word-break:break-word] flex flex-col font-['Inter:Medium',sans-serif] font-medium justify-center leading-[0] not-italic relative shrink-0 text-[#d1d5db] text-[14px] text-center whitespace-nowrap">
        <p className="leading-[20px]">Google</p>
      </div>
    </div>
  );
}

function Svg1() {
  return (
    <div className="relative shrink-0 size-[20px]" data-name="SVG">
      <svg className="absolute block inset-0 size-full" fill="none" height="20" preserveAspectRatio="none" viewBox="0 0 20 20" width="20">
        <g clipPath="url(#clip0_0_113)" id="SVG">
          <path d={svgPaths.pbb77300} fill="#D1D5DB" id="Vector" />
        </g>
        <defs>
          <clipPath id="clip0_0_113">
            <rect fill="white" height="20" width="20" />
          </clipPath>
        </defs>
      </svg>
    </div>
  );
}

function LinkedIn() {
  return (
    <div className="bg-[#242424] content-stretch drop-shadow-[0px_1px_1px_rgba(0,0,0,0.05)] flex gap-[8px] items-center justify-center px-[17px] py-[11px] relative rounded-[6px] shrink-0 w-[129.89px]" data-name="LinkedIn">
      <div aria-hidden className="absolute border border-[#374151] border-solid inset-0 pointer-events-none rounded-[6px]" />
      <Svg1 />
      <div className="[word-break:break-word] flex flex-col font-['Inter:Medium',sans-serif] font-medium justify-center leading-[0] not-italic relative shrink-0 text-[#d1d5db] text-[14px] text-center whitespace-nowrap">
        <p className="leading-[20px]">LinkedIn</p>
      </div>
    </div>
  );
}

function SocialLogins() {
  return (
    <div className="content-stretch flex gap-[16px] items-start justify-center relative shrink-0 w-full" data-name="Social Logins">
      <LinkGoogle />
      <LinkedIn />
    </div>
  );
}

function SocialLoginsMargin() {
  return (
    <div className="content-stretch flex flex-col items-start pt-[32px] relative shrink-0 w-full" data-name="Social Logins:margin">
      <SocialLogins />
    </div>
  );
}

function SignUpLink() {
  return (
    <div className="[word-break:break-word] content-stretch flex gap-[4px] items-start justify-center leading-[0] not-italic relative shrink-0 text-[14px] text-center w-full whitespace-nowrap" data-name="Sign Up Link">
      <div className="flex flex-col font-['Inter:Regular',sans-serif] font-normal justify-center relative shrink-0 text-[#9ca3af]">
        <p className="leading-[20px]">{`Don't have an account? `}</p>
      </div>
      <div className="flex flex-col font-['Inter:Medium',sans-serif] font-medium justify-center relative shrink-0 text-white">
        <p className="leading-[20px]">Request Access</p>
      </div>
    </div>
  );
}

function SignUpLinkMargin() {
  return (
    <div className="content-stretch flex flex-col items-start pt-[32px] relative shrink-0 w-full" data-name="Sign Up Link:margin">
      <SignUpLink />
    </div>
  );
}

function RightSideTheActualLoginForm() {
  return (
    <div className="absolute content-stretch flex flex-col inset-[1px_0.09%_1px_64.86%] items-start justify-center p-[64px]" data-name="Right side: The actual login form">
      <HeaderSectionOfTheFormMargin />
      <TheForm />
      <DividerMargin />
      <SocialLoginsMargin />
      <SignUpLinkMargin />
    </div>
  );
}

function MainContainer() {
  return (
    <div className="bg-[#1a1a1a] h-[713px] max-w-[1152px] relative rounded-[12px] shrink-0 w-[1152px]" data-name="MainContainer">
      <div className="overflow-clip relative rounded-[inherit] size-full">
        <Background />
        <LeftSideHeroImageTakingUpHalfTheScreenOnDesktop />
        <RightSideTheActualLoginForm />
      </div>
      <div aria-hidden className="absolute border border-[#1f2937] border-solid inset-0 pointer-events-none rounded-[12px] shadow-[0px_25px_50px_-12px_rgba(0,0,0,0.25)]" />
    </div>
  );
}

export default function StrategicLoginPage() {
  return (
    <div className="content-stretch flex items-center justify-center p-[32px] relative size-full" style={{ backgroundImage: "linear-gradient(90deg, rgb(18, 18, 18) 0%, rgb(18, 18, 18) 100%), linear-gradient(90deg, rgb(255, 255, 255) 0%, rgb(255, 255, 255) 100%)" }} data-name="Strategic Login Page">
      <MainContainer />
    </div>
  );
}