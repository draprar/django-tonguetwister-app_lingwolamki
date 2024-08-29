from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL = None
TOKENIZER = None


def load_model():
    global MODEL, TOKENIZER
    if MODEL is None or TOKENIZER is None:
        TOKENIZER = AutoTokenizer.from_pretrained("sdadas/polish-gpt2-small")
        if TOKENIZER.pad_token is None:
            TOKENIZER.pad_token = TOKENIZER.eos_token
        MODEL = AutoModelForCausalLM.from_pretrained("sdadas/polish-gpt2-small")
    return MODEL, TOKENIZER


class Chatbot:
    def __init__(self):
        self.model, self.tokenizer = load_model()
        self.keywords = {
            'rejestracja': "Aby się zarejestrować, kliknij przycisk 'Logowanie'. Zarejestruj się już teraz, aby korzystać z pełni funkcji naszej aplikacji!",
            'rejestrację': "Aby się zarejestrować, kliknij przycisk 'Logowanie'. Zarejestruj się już teraz, aby korzystać z pełni funkcji naszej aplikacji!",
            'rejestracji': "Aby się zarejestrować, kliknij przycisk 'Logowanie'. Zarejestruj się już teraz, aby korzystać z pełni funkcji naszej aplikacji!",
            'rejestracją': "Aby się zarejestrować, kliknij przycisk 'Logowanie'. Zarejestruj się już teraz, aby korzystać z pełni funkcji naszej aplikacji!",
            'kontakt': "Aby się z nami skontaktować, kliknij przycisk 'Kontakt'. Czekamy na Twoje pytania z otwartymi ramionami.",
            'kontaktu': "Aby się z nami skontaktować, kliknij przycisk 'Kontakt'. Czekamy na Twoje pytania z otwartymi ramionami.",
            'kontakcie': "Aby się z nami skontaktować, kliknij przycisk 'Kontakt'. Czekamy na Twoje pytania z otwartymi ramionami.",
            'nagrać': "Kliknij przycisk 'Nagraj swój głos', aby rozpocząć nagrywanie. Twoje nagrania są dla Ciebie ważne, aby poprawić swoje umiejętności.",
            'nagranie': "Kliknij przycisk 'Nagraj swój głos', aby rozpocząć nagrywanie. Twoje nagrania są dla Ciebie ważne, aby poprawić swoje umiejętności.",
            'nagrania': "Kliknij przycisk 'Nagraj swój głos', aby rozpocząć nagrywanie. Twoje nagrania są dla Ciebie ważne, aby poprawić swoje umiejętności.",
            'mikrofon': "Proszę zezwolić swojemu urządzeniu na używanie mikrofonu. Bez tego nie będziesz w stanie usłyszeć swoich wspaniałych prób!",
            'mikrofonu': "Proszę zezwolić swojemu urządzeniu na używanie mikrofonu. Bez tego nie będziesz w stanie usłyszeć swoich wspaniałych prób!",
            'mikrofonem': "Proszę zezwolić swojemu urządzeniu na używanie mikrofonu. Bez tego nie będziesz w stanie usłyszeć swoich wspaniałych prób!",
            'użytkownik': "Korzystaj z przycisku 'Logowanie', aby przejść do swojego konta. Twoje przygody z wymową zaczynają się tutaj!",
            'użytkownika': "Korzystaj z przycisku 'Logowanie', aby przejść do swojego konta. Twoje przygody z wymową zaczynają się tutaj!",
            'użytkownikiem': "Korzystaj z przycisku 'Logowanie', aby przejść do swojego konta. Twoje przygody z wymową zaczynają się tutaj!",
            'hasło': "Wpisz swoje hasło podczas logowania, aby uzyskać dostęp do wszystkich funkcji aplikacji.",
            'hasła': "Wpisz swoje hasło podczas logowania, aby uzyskać dostęp do wszystkich funkcji aplikacji.",
            'hasłem': "Wpisz swoje hasło podczas logowania, aby uzyskać dostęp do wszystkich funkcji aplikacji.",
            'konto': "Kliknij przycisk 'Zarejestruj się', aby założyć nowe konto i zacząć swoją podróż z LingwoŁamkami.",
            'konta': "Kliknij przycisk 'Zarejestruj się', aby założyć nowe konto i zacząć swoją podróż z LingwoŁamkami.",
            'kontem': "Kliknij przycisk 'Zarejestruj się', aby założyć nowe konto i zacząć swoją podróż z LingwoŁamkami.",
            'powrót': "Kliknij przycisk 'Wróć', aby powrócić do poprzedniego ekranu. Przemieszczaj się w aplikacji jak ryba w wodzie!",
            'powrotu': "Kliknij przycisk 'Wróć', aby powrócić do poprzedniego ekranu. Przemieszczaj się w aplikacji jak ryba w wodzie!",
            'powrotem': "Kliknij przycisk 'Wróć', aby powrócić do poprzedniego ekranu. Przemieszczaj się w aplikacji jak ryba w wodzie!",
            'lingwołamki': "Lingwołamki to aplikacja, która pomoże Ci poprawić wymowę i nabrać pewności siebie.",
            'lingwołamków': "Lingwołamki to aplikacja, która pomoże Ci poprawić wymowę i nabrać pewności siebie.",
            'lingwołamkami': "Lingwołamki to aplikacja, która pomoże Ci poprawić wymowę i nabrać pewności siebie.",
            'profil': "Kliknij przycisk 'Zarejestruj się', aby utworzyć swój profil i zacząć personalizować swoje doświadczenie.",
            'profilu': "Kliknij przycisk 'Zarejestruj się', aby utworzyć swój profil i zacząć personalizować swoje doświadczenie.",
            'profilem': "Kliknij przycisk 'Zarejestruj się', aby utworzyć swój profil i zacząć personalizować swoje doświadczenie.",
            'powtórki': "Dodawaj swoje ulubione ćwiczenia do powtórek, aby zawsze mieć je pod ręką. Ćwicz do perfekcji!",
            'powtórek': "Dodawaj swoje ulubione ćwiczenia do powtórek, aby zawsze mieć je pod ręką. Ćwicz do perfekcji!",
            'powtórkami': "Dodawaj swoje ulubione ćwiczenia do powtórek, aby zawsze mieć je pod ręką. Ćwicz do perfekcji!",
            'drukować': "Możesz wydrukować swoje ulubione ćwiczenia, klikając odpowiedni przycisk. Idealne do nauki offline!",
            'drukowania': "Możesz wydrukować swoje ulubione ćwiczenia, klikając odpowiedni przycisk. Idealne do nauki offline!",
            'drukowaniem': "Możesz wydrukować swoje ulubione ćwiczenia, klikając odpowiedni przycisk. Idealne do nauki offline!",
            'zacząć': "Przesuń palce, aby rozpocząć. Każde kliknięcie przybliża Cię do lepszej wymowy!",
            'zaczęcia': "Przesuń palce, aby rozpocząć. Każde kliknięcie przybliża Cię do lepszej wymowy!",
            'zaczęciem': "Przesuń palce, aby rozpocząć. Każde kliknięcie przybliża Cię do lepszej wymowy!",
            'problem': "Masz problem? Zapytaj naszego czata – jesteśmy tutaj, aby pomóc Ci na każdym kroku.",
            'problemu': "Masz problem? Zapytaj naszego czata – jesteśmy tutaj, aby pomóc Ci na każdym kroku.",
            'problemem': "Masz problem? Zapytaj naszego czata – jesteśmy tutaj, aby pomóc Ci na każdym kroku.",
            'artykulacyjne': "Lingwołamki to zestaw ćwiczeń artykulacyjnych, głosowych i oddechowych, które możesz wykonać samodzielnie, aby poprawić swoją wymowę.",
            'artykulacyjnych': "Lingwołamki to zestaw ćwiczeń artykulacyjnych, głosowych i oddechowych, które możesz wykonać samodzielnie, aby poprawić swoją wymowę.",
            'artykulacyjnymi': "Lingwołamki to zestaw ćwiczeń artykulacyjnych, głosowych i oddechowych, które możesz wykonać samodzielnie, aby poprawić swoją wymowę.",
            'głosowe': "Lingwołamki to zestaw ćwiczeń artykulacyjnych, głosowych i oddechowych, które możesz wykonać samodzielnie, aby poprawić swoją wymowę.",
            'głosowych': "Lingwołamki to zestaw ćwiczeń artykulacyjnych, głosowych i oddechowych, które możesz wykonać samodzielnie, aby poprawić swoją wymowę.",
            'głosowymi': "Lingwołamki to zestaw ćwiczeń artykulacyjnych, głosowych i oddechowych, które możesz wykonać samodzielnie, aby poprawić swoją wymowę.",
            'oddechowe': "Lingwołamki to zestaw ćwiczeń artykulacyjnych, głosowych i oddechowych, które możesz wykonać samodzielnie, aby poprawić swoją wymowę.",
            'oddechowych': "Lingwołamki to zestaw ćwiczeń artykulacyjnych, głosowych i oddechowych, które możesz wykonać samodzielnie, aby poprawić swoją wymowę.",
            'oddechowymi': "Lingwołamki to zestaw ćwiczeń artykulacyjnych, głosowych i oddechowych, które możesz wykonać samodzielnie, aby poprawić swoją wymowę.",
            'lusterko': "Kliknij przycisk 'Otwórz Lusterko', aby sprawdzić swoje ruchy w lustrze podczas ćwiczeń. Bądź swoim własnym trenerem!",
            'lusterka': "Kliknij przycisk 'Otwórz Lusterko', aby sprawdzić swoje ruchy w lustrze podczas ćwiczeń. Bądź swoim własnym trenerem!",
            'lusterkiem': "Kliknij przycisk 'Otwórz Lusterko', aby sprawdzić swoje ruchy w lustrze podczas ćwiczeń. Bądź swoim własnym trenerem!",
            'zemsta': "Zemsta logopedy to łamańce językowe, które znajdziesz w aplikacji Lingwołamki. Czy jesteś gotów na wyzwanie?",
            'zemście': "Zemsta logopedy to łamańce językowe, które znajdziesz w aplikacji Lingwołamki. Czy jesteś gotów na wyzwanie?",
            'zemstą': "Zemsta logopedy to łamańce językowe, które znajdziesz w aplikacji Lingwołamki. Czy jesteś gotów na wyzwanie?",
            'logopedy': "Zemsta logopedy to łamańce językowe, które znajdziesz w aplikacji Lingwołamki. Czy jesteś gotów na wyzwanie?",
            'logopedzie': "Zemsta logopedy to łamańce językowe, które znajdziesz w aplikacji Lingwołamki. Czy jesteś gotów na wyzwanie?",
            'logopedą': "Zemsta logopedy to łamańce językowe, które znajdziesz w aplikacji Lingwołamki. Czy jesteś gotów na wyzwanie?",
            'awatar': "Kliknij przycisk 'Zarządzaj Awatarem', aby dostosować swoje zdjęcie profilowe. Pokaż światu, kim jesteś!",
            'awatarem': "Kliknij przycisk 'Zarządzaj Awatarem', aby dostosować swoje zdjęcie profilowe. Pokaż światu, kim jesteś!",
            'awatara': "Kliknij przycisk 'Zarządzaj Awatarem', aby dostosować swoje zdjęcie profilowe. Pokaż światu, kim jesteś!",
            'zdjęcie': "Kliknij przycisk 'Zarządzaj Awatarem', aby dostosować swoje zdjęcie profilowe. Pokaż światu, kim jesteś!",
            'zdjęcia': "Kliknij przycisk 'Zarządzaj Awatarem', aby dostosować swoje zdjęcie profilowe. Pokaż światu, kim jesteś!",
            'zdjęciem': "Kliknij przycisk 'Zarządzaj Awatarem', aby dostosować swoje zdjęcie profilowe. Pokaż światu, kim jesteś!",
            'zapisać': "Kliknij przycisk 'Eksportuj Ćwiczenia do PDF', aby zapisać swoje ćwiczenia w formacie PDF. Idealne do późniejszego przeglądania.",
            'zapisania': "Kliknij przycisk 'Eksportuj Ćwiczenia do PDF', aby zapisać swoje ćwiczenia w formacie PDF. Idealne do późniejszego przeglądania.",
            'zapisaniem': "Kliknij przycisk 'Eksportuj Ćwiczenia do PDF', aby zapisać swoje ćwiczenia w formacie PDF. Idealne do późniejszego przeglądania.",
            'staropolszczyzna': "Dzięki aplikacji Lingwołamki poznasz staropolskie słowa i zwroty. Przenieś się w czasie i odkryj bogactwo polskiego języka!",
            'staropolszczyzny': "Dzięki aplikacji Lingwołamki poznasz staropolskie słowa i zwroty. Przenieś się w czasie i odkryj bogactwo polskiego języka!",
            'staropolszczyzną': "Dzięki aplikacji Lingwołamki poznasz staropolskie słowa i zwroty. Przenieś się w czasie i odkryj bogactwo polskiego języka!",
            'twórca': "Pomysł na stworzenie Lingwołamków zrodził się w głowach Michała i Pauliny. Dzięki nim możesz teraz poprawiać swoją wymowę w zabawny sposób!",
            'twórcy': "Pomysł na stworzenie Lingwołamków zrodził się w głowach Michała i Pauliny. Dzięki nim możesz teraz poprawiać swoją wymowę w zabawny sposób!",
            'twórcą': "Pomysł na stworzenie Lingwołamków zrodził się w głowach Michała i Pauliny. Dzięki nim możesz teraz poprawiać swoją wymowę w zabawny sposób!",
            'ćwiczenia': "Lingwołamki to aplikacja, w której znajdziesz różnorodne ćwiczenia poprawiające Twoją wymowę. Ćwicz z nami i stań się mistrzem języka!",
            'ćwiczeń': "Lingwołamki to aplikacja, w której znajdziesz różnorodne ćwiczenia poprawiające Twoją wymowę. Ćwicz z nami i stań się mistrzem języka!",
            'ćwiczeniami': "Lingwołamki to aplikacja, w której znajdziesz różnorodne ćwiczenia poprawiające Twoją wymowę. Ćwicz z nami i stań się mistrzem języka!",
            'łamańce': "Lingwołamki to aplikacja z unikalnymi łamańcami językowymi, które sprawią, że Twoja wymowa będzie precyzyjna jak nigdy wcześniej.",
            'łamańców': "Lingwołamki to aplikacja z unikalnymi łamańcami językowymi, które sprawią, że Twoja wymowa będzie precyzyjna jak nigdy wcześniej.",
            'łamańcami': "Lingwołamki to aplikacja z unikalnymi łamańcami językowymi, które sprawią, że Twoja wymowa będzie precyzyjna jak nigdy wcześniej.",
            'trudne': "W Lingwołamkach znajdziesz zestawy trudnych słów, które pomogą Ci pokonać najbardziej wymagające wyzwania językowe.",
            'słowa': "W Lingwołamkach znajdziesz zestawy trudnych słów, które pomogą Ci pokonać najbardziej wymagające wyzwania językowe.",
            'powtarzanie': "Powtarzaj ćwiczenia, aby utrwalić nowe umiejętności i być pewnym swojej wymowy w każdej sytuacji.",
            'powtarzania': "Powtarzaj ćwiczenia, aby utrwalić nowe umiejętności i być pewnym swojej wymowy w każdej sytuacji.",
            'powtarzaniem': "Powtarzaj ćwiczenia, aby utrwalić nowe umiejętności i być pewnym swojej wymowy w każdej sytuacji.",
            'samodzielna': "Lingwołamki to idealne narzędzie do samodzielnej nauki. Ćwicz, kiedy chcesz i jak chcesz!",
            'nauka': "Lingwołamki to idealne narzędzie do samodzielnej nauki. Ćwicz, kiedy chcesz i jak chcesz!",
            'logowanie': "Logowanie jest proste i szybkie. Kliknij 'Zaloguj się', aby wrócić do swoich ulubionych ćwiczeń.",
            'logowania': "Logowanie jest proste i szybkie. Kliknij 'Zaloguj się', aby wrócić do swoich ulubionych ćwiczeń.",
            'logowaniem': "Logowanie jest proste i szybkie. Kliknij 'Zaloguj się', aby wrócić do swoich ulubionych ćwiczeń.",
            'poradniki': "Skorzystaj z naszych poradników, aby dowiedzieć się, jak w pełni wykorzystać możliwości Lingwołamków.",
            'poradników': "Skorzystaj z naszych poradników, aby dowiedzieć się, jak w pełni wykorzystać możliwości Lingwołamków.",
            'poradnikami': "Skorzystaj z naszych poradników, aby dowiedzieć się, jak w pełni wykorzystać możliwości Lingwołamków.",
            'ćwiczenia głosowe': "Pracuj nad swoim głosem z pomocą naszych ćwiczeń głosowych. Zostań mistrzem dykcji!",
            'ćwiczeń głosowych': "Pracuj nad swoim głosem z pomocą naszych ćwiczeń głosowych. Zostań mistrzem dykcji!",
            'głosowych ćwiczeń': "Pracuj nad swoim głosem z pomocą naszych ćwiczeń głosowych. Zostań mistrzem dykcji!",
            'edytuj': "Edytuj swój profil użytkownika, aby dostosować doświadczenie w aplikacji do swoich potrzeb.",
            'profilu użytkownika': "Edytuj swój profil użytkownika, aby dostosować doświadczenie w aplikacji do swoich potrzeb.",
            'profili': "Edytuj swój profil użytkownika, aby dostosować doświadczenie w aplikacji do swoich potrzeb.",
            'zadań domowych': "Ustal zadania domowe, aby regularnie ćwiczyć i utrwalać nowo nabyte umiejętności.",
            'zadania domowe': "Ustal zadania domowe, aby regularnie ćwiczyć i utrwalać nowo nabyte umiejętności.",
            'domowe zadania': "Ustal zadania domowe, aby regularnie ćwiczyć i utrwalać nowo nabyte umiejętności.",
            'nauki': "Włącz tryb nauki, aby skoncentrować się na jednym aspekcie wymowy i doskonalić swoje umiejętności krok po kroku.",
            'trybu': "Włącz tryb nauki, aby skoncentrować się na jednym aspekcie wymowy i doskonalić swoje umiejętności krok po kroku.",
            'nauką': "Włącz tryb nauki, aby skoncentrować się na jednym aspekcie wymowy i doskonalić swoje umiejętności krok po kroku.",
            'trybem': "Włącz tryb nauki, aby skoncentrować się na jednym aspekcie wymowy i doskonalić swoje umiejętności krok po kroku.",
            'wynikiem': "Podziel się swoim wynikiem z przyjaciółmi lub logopedą. Pochwal się swoimi postępami!",
            'wyniku': "Podziel się swoim wynikiem z przyjaciółmi lub logopedą. Pochwal się swoimi postępami!",
            'lekcji': "Skorzystaj z naszych lekcji online, aby uzyskać dodatkowe wskazówki i poprawić swoją wymowę.",
            'lekcje': "Skorzystaj z naszych lekcji online, aby uzyskać dodatkowe wskazówki i poprawić swoją wymowę.",
            'online': "Skorzystaj z naszych lekcji online, aby uzyskać dodatkowe wskazówki i poprawić swoją wymowę.",
            'katalogu': "Przeglądaj nasz katalog ćwiczeń i wybieraj te, które najbardziej odpowiadają Twoim potrzebom.",
            'katalog': "Przeglądaj nasz katalog ćwiczeń i wybieraj te, które najbardziej odpowiadają Twoim potrzebom.",
            'poprawy': "Popraw swoją wymowę dzięki regularnym ćwiczeniom z Lingwołamkami. Każde ćwiczenie to krok naprzód!",
            'poprawa': "Popraw swoją wymowę dzięki regularnym ćwiczeniom z Lingwołamkami. Każde ćwiczenie to krok naprzód!",
            'rozgrzewki': "Rozgrzej swoje narządy mowy przed ćwiczeniami, aby uzyskać najlepsze rezultaty.",
            'rozgrzewka': "Rozgrzej swoje narządy mowy przed ćwiczeniami, aby uzyskać najlepsze rezultaty.",
            'sprawdzenia': "Sprawdź swoją wymowę i porównaj ją z wzorcowymi nagraniami. Ucz się na błędach!",
            'sprawdź': "Sprawdź swoją wymowę i porównaj ją z wzorcowymi nagraniami. Ucz się na błędach!",
            'nauk': "Lingwołamki łączą naukę z zabawą. Ćwicz wymowę i jednocześnie baw się dobrze!",
            'zabawę': "Lingwołamki łączą naukę z zabawą. Ćwicz wymowę i jednocześnie baw się dobrze!",
            'dziennika': "Prowadź dziennik postępów, aby śledzić swoje osiągnięcia i wyznaczać nowe cele.",
            'dziennik': "Prowadź dziennik postępów, aby śledzić swoje osiągnięcia i wyznaczać nowe cele.",
            'wyzwań': "Staw czoła wyzwaniom logopedycznym, które sprawdzą Twoje umiejętności i pomogą je doskonalić.",
            'wyzwania': "Staw czoła wyzwaniom logopedycznym, które sprawdzą Twoje umiejętności i pomogą je doskonalić.",
            'celów': "Ustal swoje cele w aplikacji i realizuj je krok po kroku. Każdy cel to kolejny sukces!",
            'cele': "Ustal swoje cele w aplikacji i realizuj je krok po kroku. Każdy cel to kolejny sukces!",
            'instrukcji': "Przeczytaj instrukcje przed rozpoczęciem ćwiczeń, aby dokładnie wiedzieć, jak je wykonać.",
            'instrukcje': "Przeczytaj instrukcje przed rozpoczęciem ćwiczeń, aby dokładnie wiedzieć, jak je wykonać.",
            'wsparcia': "Korzystaj z naszego wsparcia logopedycznego, aby lepiej zrozumieć swoje potrzeby i osiągnąć sukces.",
            'wsparcie': "Korzystaj z naszego wsparcia logopedycznego, aby lepiej zrozumieć swoje potrzeby i osiągnąć sukces.",
            'postępami': "Udostępniaj swoje postępy z innymi, aby wspólnie motywować się do dalszej pracy.",
            'postępy': "Udostępniaj swoje postępy z innymi, aby wspólnie motywować się do dalszej pracy.",
            'specjalnych': "Sprawdź nasze ćwiczenia specjalne, zaprojektowane z myślą o zaawansowanych użytkownikach.",
            'specjalne': "Sprawdź nasze ćwiczenia specjalne, zaprojektowane z myślą o zaawansowanych użytkownikach.",
            'zaplanowanych': "Planowanie sesji ćwiczeniowych pomoże Ci w regularnej praktyce i osiągnięciu zamierzonych celów.",
            'sesji': "Planowanie sesji ćwiczeniowych pomoże Ci w regularnej praktyce i osiągnięciu zamierzonych celów.",
            'pomoc': "Jeśli potrzebujesz pomocy, odwiedź sekcję 'Kontakt' lub skontaktuj się z nami bezpośrednio.",
            'pomocy': "Jeśli potrzebujesz pomocy, odwiedź sekcję 'Kontakt' lub skontaktuj się z nami bezpośrednio.",
            'kurs': "Lingwołamki oferują specjalistyczne kursy wymowy, które pomogą Ci w opanowaniu trudnych aspektów mowy.",
            'kursy': "Lingwołamki oferują specjalistyczne kursy wymowy, które pomogą Ci w opanowaniu trudnych aspektów mowy."
        }

    def generate_response(self, input_text):
        if self.tokenizer.pad_token is None:
            custom_pad_token = "[PAD]"
            self.tokenizer.add_special_tokens({'pad_token': custom_pad_token})

        inputs = self.tokenizer(input_text, return_tensors='pt', padding=True, truncation=True, max_length=50)

        input_ids = inputs['input_ids']
        attention_mask = inputs['attention_mask']

        output = self.model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_length=50,
            num_return_sequences=1,
            repetition_penalty=2.0,
            no_repeat_ngram_size=2,
            pad_token_id=self.tokenizer.pad_token_id,
        )

        response = self.tokenizer.decode(output[0], clean_up_tokenization_spaces=True, skip_special_tokens=True)

        if input_text in response:
            response = response.replace(input_text, "").strip()

        return response

    def get_response(self, user_input):
        for keyword, response in self.keywords.items():
            if keyword in user_input.lower():
                return response
        return self.generate_response(user_input)
