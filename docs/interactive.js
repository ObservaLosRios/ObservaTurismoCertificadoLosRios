document.addEventListener('DOMContentLoaded', () => {
	const navLinks = Array.from(document.querySelectorAll('.nav-link[data-target]'));
	const sections = Array.from(document.querySelectorAll('.section'));

	const showSection = (targetId) => {
		sections.forEach((section) => {
			section.classList.toggle('active', section.id === targetId);
		});

		navLinks.forEach((link) => {
			link.classList.toggle('active', link.dataset.target === targetId);
		});
	};

	navLinks.forEach((link) => {
		const targetId = link.dataset.target;
		const activate = () => showSection(targetId);
		link.addEventListener('click', activate);
		link.addEventListener('keypress', (event) => {
			if (event.key === 'Enter' || event.key === ' ') {
				event.preventDefault();
				activate();
			}
		});
	});
});
