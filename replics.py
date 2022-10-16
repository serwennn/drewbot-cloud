replic = {

    "help": ["Вызов информации о команде/командах.", "`d!help <название команды>`\n`d!help kick`", "Фырк, очень странно смотреть информацию о команде просмотра информации..."],
    "info": ["Информация и Статистика бота.", "`d!info`", "Информация о текущей версии бота, даты релиза последнего обновления, текущий префикс на сервере, кол-во людей и севреров где он находится."],
    "ping": ["Текущий пинг бота.", "d!ping", "Текущий пинг API для Discord, нак котором написан бот."],
    
    'mute': ["Даёт мьют(таймаут) участнику на указанное время.", "`d!mute (участник) (время) <причина>`\n`d!mute @seltfox 15m Съел все печеньки!`", "Даёт мьют(Вшитый в Discord таймаут) от 1 секунды до 28 дней включительно. Во время пробывания в мьюте(таймауте), участник не может писать сообщения, ставить реакции, создавать ветки и писать в них, а так же находится в голосовых каналах."],
    'unmute': ["Снимает мьют(таймаут) с участника.", "`d!unmute (участник) <причина>`\n`d!unmute @seltfox Обещал купить новые печеньки.`", "Снимает мьют(Вшитый в Discord таймаут) с участника. Вы можете указать причину снятия мьюта, которая будет указана в сообщении и в журнале аудита."],
    'kick': ["Кикает участника с сервера.", "`d!kick (участник) <причина>`\n`d!kick @seltfox Не купил печеньки!`", "Участник может вернутся на сервер, если у него есть ссылка-приглашение на сервер. Все сообщения участника не будут удалены."],
    'ban': ["Банит участника.", "`d!ban (участник) <причина>`\n`d!ban @seltfox ЪЙЦБЩШСЯЦХЪъ`", "Банит участника с сервера. Забаненый пользователь не сможет вернутся на сервер, пока с него не снимут бан. Все сообщения участника не будут удалены."],
    'unban': ["Снимает бан с пользователя.", "`d!unban (ID пользователя) <причина>`\n`d!unban 735371414533701672 Извинился.`", "Снимает бан с указанного пользователя. Для снятия бана с пользователя, вы должны ввести его ID. Чтобы скопирповать ID пользователя включите Инструменты Разработчика в настройках аккаунта, и затем перейдите на профиль пользователя."],

    'server': ["Информация о текущем сервере.;;`d!server`;;Отправляет подробную информацию о текущем сервере."],
    'user': ["Информация о указаном участнике.;;`d!user <участник>`\n`d!user @seltfox`;;Отправляет информацию о профиле укзанного участника."],
    'avatar': ["Отправляет аватар указаного участника.;;`d!avatar <участник>`\n`d!avatar @seltfox`;;Отправляет аватар указаного участника в его оригинальном разрешении. Довольно красиво!"],
    
    'whitelist': ["Заносит/Вычеркивает участника из белого списка сервера.", "`Команда отключена`", "Извините, но вайтлист система скоро будет удалена из бота, из-за её несовершенности и непрактичности в использовании. Мы будем стараться улучшать её, и возможно вскоре вернём её обратно."],
    'reactionrole': ["Создает экземпляр роли за реакцию.", "`d!reactionrole <add | remove> (ID сообщения) (ID роли) (Эмодзи)`\n`d!reactionrole`\n`d!reactionrole add 1014640756885037148 897718755461853194 ❤️`", "Добавляет/Удаляет экземпляр роли за реакцию. Если оставить без аргументов, то показывает текущий список экзепляров ролей за реакцию этого сервера. Для использования команды вы должны быть владельцем сервера или быть в белом списке сервера (Вайтлист).\n**Что такое роли за реакцию?** Проще говоря, роли за реакцию — это сообщение, с одной или несколькими реакциями, нажимая на которую вы получаете какую-либо роль. Это очень удобно если вам нужно сделать верификацию на сервере, или же сделать выбор ролей."],
    'autorole': ["Создает экземпляр автороли.", "`d!autorole <add | remove> (ID роли)`\n`d!autorole`\n`d!autorole add 897718755461853194`", "Добаляет/Удаляет экземпляр автороли на сервере. Если оставить без аргументов, то показывает текущий список экзепляров авторолей этого сервера. Для использования команды вы должны быть владельцем сервера или быть в белом списке сервера (Вайтлист).\n**Что такое автороли?** Автороли — это роли, которые выдаются пользователю, при входе на сервер."],
    'anticrash': ["Анти-краш система", "`Команда отключена`", "Извините, но анти-краш система скоро будет удалена из бота, из-за её несовершенности и непрактичности в использовании. Мы будем стараться улучшать её, и возможно вскоре вернём её обратно."],

    'fox': ["Отправляет случайное фото лисы! ヾ(•ω• )o", "d!fox", "Все любят этих милых и пушистых зверушек! Фыр-фыр!"],
    'cat': ["Отправляет случайное фото кошечки! ᓚᘏᗢ", "d!cat", "Эта команда покажет вам фото самых милых кошечек! o((>ω< ))o"],
    'dog': ["Отправляет случайное фото пёселя! ^-^", "d!dog", "Собачки? Пёсики? Эта команда отлично подойдет для фанатов четвероногих любителей косточек!"],


    "blacklist_error": ["💫** : Во дела...**", "Вам запрещено пользоваться всеми функциями бота (Добавлять его на свой сервер, и использовать его комманды на других серверах) так как вы были занесены в черный список бота.\n**🦊 : Полезные ссылки:**\n[Условия использования DrewBot](https://drewsupport.github.io/terms)\n[Сервер поддержки DrewBot](https://discord.gg/B9mQ26fCWN)"],
    "unk_error": "Неизвестная ошибка. Возможно вам поможет:\n**☀️ : Проверьте права на данное действие и права Администратора у роли бота.\n✨ : Поставьте роль бота как можно выше.\n🗝️ : Проверьте правильность введённых данных.**",
    "error": "💥 : Ошибка!",

    'loading': ["На балу пляшут шуты...", "Пока идёт загрузка, тут появляются отсылки на многое.", "Думаем над тем что ответить...", "Почеши мне хвостик.", "Обычная загрузка...", "Необычная загрузка!", "Я никогда не сплю. (шутка)", "Хотите анекдот?", "Раньше у меня был друг с желтым клювом. Не знаю куда он пропал.", "Бродя сквозь густые леса можно наткнуться на лисью берлогу програ... Нет, это не реклама.",
                "Виляем хвостиком...", "фыр фыр фыр фыр фыр фыр фыр фыр фыр фыр фыр фыр фыр фыр фыр фыр фыр фыр фыр фыр"]
}