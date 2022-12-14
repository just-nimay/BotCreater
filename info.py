
class Information():
	INFO = '''
	========
	<u>Информация</u>
	---
	 Чтобы создать коллецию тебе нужно:
	    • Ваши изображения, которые должы быть нарисованы таким образом, чтобы при наложении их друг на друга получалась правильная картинка
	    • изображения дожны быть формата  <b>png</b> с прозрачным фоном (кроме самого фона)
	    • Вам нужно несколько изображений различных признаков. Например: три рубашки разного цвета, три вида прически и т.д.
	    (<b>будьте внимательны при создания имени ваших изображений</b>: название этих изображений будет в файле метаданых)

	----
	<u>Этапы создания</u>

	После нажатия кнопки <i>"создать  генеративную коллекцию🛠"</i> вы должны будете ввести название вашей коллекции (название должно быть на английском языке). 

	После, нажимайте кнопку <i>"Новый слой❇️"</i> для того что бы добавить новый слой. После этого Бот попросит вас ввести названия слоя (название должно быть на английском языке).

	Далее нужно будет указать порядковый номер слоя. Что такое порядковый номер слоя? Сейчас объясню. Допустим, у вас имеется слой <i>Фон</i> и он имеет порядковый номер 1. Так же у вас есть слой <i>Лицо</i> с порядковым номером 2. При создании полноценного изображения из этих слоёв, слой <i>Лицо</i> будет "на" слое <i>Фон</i>. Если же у этих слоёв порядковые номера были наоборот, то тогда бы мы не увидели слой <i>Лицо</i>, т.к. он был бы уровнем ниже.

	Затем нужно указать обязательность. Опять всё непонятно? Итак, <b>Обязательность</b> ⏤ это, другими словами, обязательность появления слоя: определенные слои (например, фон, тело и глаза) должны присутствовать в каждом изображении, в то время как некоторые другие слои (например, головной убор, браслет или одежда) могут быть необязательными. Рекомендуется первому (фоновому) слою быть обязательно.

	----
	<u>Добавление изображений</u>

	После того как вы создали слой, вы можете добавить изображение, нажав кнопку <i>Добавить изображения(-е)🖼</i>. После того как вы отправили нужные вам изображения, напишите боту "<i>готово</i>".
	Если же после создания слоя и добавления изображений вы поняли, что вы добавили не все изображения, то вам следует нажать кнопку <i>Мои слои💎</i>, далее нажмите <i>Настроить слои🔧</i>, затем выберите интересующий вас слой, и нажмите <i>Добавить изображения(-е)🖼</i>

    ----
    <u>Настройка слоёв</u>

    Если вы уже создали несколько слоёв, и нажали кнопку <i>Мои слои💎</i>, вам выведутся ваши слои. Если вы заметили, что с одним из слоёв что-то не так и хотите это изменить, смело нажимайте кнопку <i>Настроить слои🔧</i>, затем выберите интересующий вас слой, и выбирите интересующий вас пункт.
	----
	<u>Генерация коллекции</u>

	После того как вы создали и настроили слои, добавили изображения, можно приступать к самому интересному: генерации коллекции.
	Для этого в главном меню нажмите кнопку <i>"сгенерировать"</i>. После вам будет показано <b>максимальное</b> колличество возможных комбинаций изображений. Введите число изображений, <b><i>не привышающее максимальное колличество</i></b> возможных комбинаций.
	После этого начнется процесс создания коллекции. Это может занять некоторое время.

	После окончания процесса генерации, вам нужно будет нажать на кнопку <i>"скачать"</i>, после чего вам будет отпрвлен архив с изображениями и файлом метаданных в формате  CSV, который вы смлжете открыть в приложении Exel (или ей подобной) и проанализировать частоту появления каких-либо черт, комбинаций

	----
	<u>От разаботчика</u>

	Этот бот генирирует изображения с помощью библиотеки для Python с открытым исходным кодом, которая была написана другим разработчиком.
	GitHub разработчика библиотеки: https://github.com/rounakbanik
	GitHub библиотеки: https://github.com/rounakbanik/generative-art-nft
	Спасибо ему большое!

	Если вы обнаружили какие-то недоработки и ошибки, присылайте на адрес <code>example@mail.com</code>
	 Благодарю за использование этого бота :)
	'''
n = 0
